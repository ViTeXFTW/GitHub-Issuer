import discord
from discord import app_commands
from discord.ext import commands
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
REPO_OWNER = os.getenv("REPO_OWNER")
REPO_NAME = os.getenv("REPO_NAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")
CHANNEL_ID = os.getenv("CHANNEL_ID")


class BugBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        intents.message_content = True
        super().__init__(command_prefix="/", intents=intents)
        self.guild_id = GUILD_ID  # Store the guild ID for easier access

    async def setup_hook(self):
        # Register commands to the specified guild
        guild = discord.Object(id=self.guild_id)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)

# Initialize the bot
bot = BugBot()

def create_github_issue(title, body, labels):
    """Function to create a GitHub issue with a title, body, and labels."""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    data = {
        "title": title,
        "body": body,
        "labels": labels,
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        return response.json()["html_url"]
    else:
        print(f"Failed to create issue: {response.status_code}, {response.text}")
        return None

@bot.tree.command(name="bug", description="Create a GitHub issue with title, labels, and a description.")
@app_commands.describe(
    title="Title of the issue",
    body="Description of the issue"
)
async def bug(interaction: discord.Interaction, title: str, body: str):
    """
    Slash command function that interacts with GitHub API to create an issue.
    """
    # Call the GitHub API function
    issue_url = create_github_issue(title, body, ["bug"])
    if issue_url:
        response_message = f"Issue created successfully: {issue_url}"
    else:
        response_message = "Failed to create issue. Please check the bot's permissions and repository settings."

    await interaction.response.send_message(response_message, delete_after=600)

# Run the bot
bot.run(BOT_TOKEN)