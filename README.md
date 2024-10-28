# Discord AI Bot

This Discord bot, named Atreyu, is a versatile AI-powered assistant designed for Ron's personal Discord server. It uses OpenAI's GPT models to provide helpful and friendly responses to user queries.

## Features

- AI-powered conversations using OpenAI's GPT models
- Custom commands for server management
- Integration with LangChain for enhanced AI capabilities
- Token usage tracking and cost estimation

## Requirements

- Python 3.7+
- Discord.py library
- OpenAI API key
- LangChain API key
- Discord Bot Token

## Installation

1. Clone the repository:

   ```bash
   git clone cd Discord_Bot

   ```

2. Install required packages:

   ```bash
   pip install discord.py python-dotenv openai langchain

   ```

3. Set up environment variables:
   Create a `.env` file in the project root and add the following:
   OPENAI_API_KEY=your_openai_api_key
   DISCORD_TOKEN=your_discord_bot_token
   LANGCHAIN_API_KEY=your_langchain_api_key

## Usage

1. Run the bot:

   ```bash
    python discordAIBot.py
   ```

2. Interact with the bot in your Discord server:

- Mention the bot or use the `!bot` prefix to start a conversation
- Use `!help` to see available commands
- Use `!rules` to display server rules

## Custom Commands

- `!joined @user`: Displays when a mentioned user joined the server
- `!guess <number>`: Play a guessing game with numbers 1-6

## AI Conversation

The bot uses OpenAI's GPT models to generate responses. It's designed to be friendly, casual, and use Discord-style formatting for clarity.

## LangChain Integration

The bot leverages LangChain for enhanced AI capabilities and conversation management. It uses the LangChain Hub to pull prompts and the OpenAI callback manager for token usage tracking.

## Token Usage and Cost Tracking

The bot tracks token usage and estimates the cost of each interaction, printing this information to the console.

## Customization

You can customize the bot's behavior by modifying the `discordAIBot.py` file:

- Adjust the `SystemMessage` content to change the bot's personality
- Modify existing commands or add new ones in the `DiscordBot` class
- Change the AI model by updating the `model_name` in the `ChatOpenAI` initialization

## Troubleshooting

If you encounter any issues, check the console output for error messages. Ensure all required environment variables are set correctly and that your Discord bot has the necessary permissions in your server.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This bot is for personal use and should be used responsibly. Ensure compliance with Discord's Terms of Service and OpenAI's use-case policies.
