import os
import random
import uuid
import json
import re
from dotenv import load_dotenv
from discord.ext import commands
import discord
import asyncio
from openai import OpenAI
from langchain import hub
from langchain_openai import ChatOpenAI
import langchain
from langchain_community.callbacks.manager import get_openai_callback
from langchain.schema import HumanMessage, AIMessage, SystemMessage


# Load environment variables
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
discord_key = os.getenv("DISCORD_TOKEN")

# Set up OpenAI client
openai_client = OpenAI(api_key=openai_key)

# set the LANGCHAIN_API_KEY environment variable (create key in settings)
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Discord Bot"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")


class DiscordBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)
        self.hub_prompt = hub.pull("discord_bot")
        self.llm = ChatOpenAI(model_name="gpt-4o-mini")

    async def on_ready(self):
        print(f"Logged in as {self.user}")

    @commands.command()
    async def joined(self, ctx, member: discord.Member):
        """Says when a member joined."""
        await ctx.send(
            f"{member.name} joined {discord.utils.format_dt(member.joined_at)}"
        )

    @commands.command()
    async def guess(self, ctx, number: int):
        """Guess a random number from 1 to 6."""
        value = random.randint(1, 6)
        await ctx.send("✅" if number == value else "❌")

    def clean_message(self, message):
        cleaned = message.content.replace(f"<@!{self.user.id}>", "").strip()
        cleaned = cleaned.replace("!bot", "").strip()
        return cleaned

    async def on_message(self, message):
        if message.author == self.user:
            return

        print(f"Message from {message.author}: {message.content}")

        if self.user.mentioned_in(message) or message.content.startswith("!bot"):
            try:
                cleaned_message = self.clean_message(message)
                formatted_prompt = self.hub_prompt.format(user_input=cleaned_message)

                with get_openai_callback() as cb:
                    run_id = str(uuid.uuid4())
                    cb.on_chain_start(
                        {"name": "DiscordBot"},
                        {"input": formatted_prompt},
                        run_id=run_id,
                    )

                    messages = [
                        SystemMessage(
                            content="You are a helpful assistant named Atreyu for Ron's personal Discord server. Be friendly and casual, using occasional emojis where appropriate. Give concise responses by default, expand only when asked. Use Discord-style formatting (code blocks, bullet points) for clarity."
                        ),
                        HumanMessage(content=formatted_prompt),
                    ]
                    response = self.llm.invoke(messages)

                    # Extract content from AIMessage
                    if isinstance(response, AIMessage):
                        bot_response = response.content
                    else:
                        bot_response = str(response)

                    # Clean up the response
                    bot_response = self.clean_response(bot_response)

                    cb.on_chain_end({"output": bot_response}, run_id=run_id)

                    print(f"Total Tokens: {cb.total_tokens}")
                    print(f"Prompt Tokens: {cb.prompt_tokens}")
                    print(f"Completion Tokens: {cb.completion_tokens}")
                    print(f"Total Cost (USD): ${cb.total_cost}")

                # Handle special commands
                if cleaned_message.lower() == "!help":
                    bot_response = "Available commands:\n!help: Show available commands\n!rules: Display server rules"
                elif cleaned_message.lower() == "!rules":
                    bot_response = "Server rules: [Insert your server rules here]"

                await message.channel.send(bot_response)
            except Exception as e:
                print(f"An error occurred: {e}")
                await message.channel.send(
                    "Sorry, I encountered an error while processing your request."
                )

        await self.process_commands(message)

    def clean_response(self, response):
        # Remove any JSON-like structures
        cleaned = re.sub(r"\{.*?\}", "", response, flags=re.DOTALL)
        # Remove any remaining metadata-like content
        cleaned = re.sub(r"additional_kwargs.*", "", cleaned, flags=re.DOTALL)
        # Strip whitespace and newlines
        cleaned = cleaned.strip()
        return cleaned


# Create bot instance
bot = DiscordBot()

# Run the Discord bot
bot.run(discord_key)
