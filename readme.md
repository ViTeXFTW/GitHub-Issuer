# GitHub Issue Creator Discord Bot

This Discord bot allows users to create GitHub issues directly from Discord using slash commands.

## Features

- **Create GitHub Issues**: Users can create issues on a specified GitHub repository by providing a title, labels, and a description through a slash command.

## Setup Instructions

### Prerequisites

1. **Python 3.8+** installed on your machine.
2. **Discord Bot Token** from the [Discord Developer Portal](https://discord.com/developers/applications).
3. **GitHub Personal Access Token** with `repo` or `public_repo` permissions. You can create one from [GitHub Developer Settings](https://github.com/settings/tokens).
4. **Channel and Guild IDs** from Discord:
   - Enable Developer Mode in Discord, then right-click on your server (guild) and channel to copy their IDs.

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/ViTeXFTW/GitHub-Issuer.git
   cd GitHub-Issuer
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file and add your Discord bot token, GitHub personal access token, guild ID, and channel ID:
   ```bash
   DISCORD_TOKEN=your_discord_bot_token
   GITHUB_TOKEN=your_github_personal_access_token
   GUILD_ID=your_guild_id
   CHANNEL_ID=your_channel_id
   ```

4. Run the bot:
   ```bash
   python bot.py
   ```

### Usage

- Use the `/bug` slash command to create a GitHub issue.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
