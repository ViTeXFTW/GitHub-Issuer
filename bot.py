import discord
from discord import app_commands
from discord.ext import commands
import requests
import os


# Retrieve sensitive information from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_OWNER = os.getenv("REPO_OWNER")
REPO_NAME = os.getenv("REPO_NAME")
FORUM_CHANNEL_ID = os.getenv("FORUM_CHANNEL_ID") # ID of the forum channel
TAG_NAME = "bug"  # The tag name to check for


class BugBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True  # Required to read message content
        intents.guilds = True  # Required for detecting new threads in forum channels
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Sync the slash commands with the guild (server)
        guild = discord.Object(id=os.getenv("GUILD_ID"))
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)
        print(f"Bot is ready and commands are synced for guild {guild.id}!")

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    def create_github_issue(self, title, body, labels):
        """Function to create a GitHub issue with a title, body, and labels."""
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
        }
        data = {
            "title": title,
            "body": body,
            "labels": labels,  # Adding labels to the issue
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            return response.json()["html_url"]
        else:
            print(f"Failed to create issue: {response.status_code}, {response.text}")
            return None

bot = BugBot()

@bot.tree.command(name="bug", description="Create a GitHub issue with the 'issued' tag.")
async def bug_command(interaction: discord.Interaction):
    """
    This command will create a GitHub issue with the 'bug' label from the post's content.
    """
    # Ensure the command is executed in a thread (forum post)
    if not isinstance(interaction.channel, discord.Thread):
        await interaction.response.send_message("This command can only be used within a forum post.", ephemeral=True)
        return

    thread = interaction.channel  # The current thread (post)
    
    # Get the first message in the thread (usually the post body)
    try:
        first_message = await thread.fetch_message(thread.id)
    except discord.NotFound:
        await interaction.response.send_message("Could not find the first message in this thread.", ephemeral=True)
        return

    # Prepare the GitHub issue content
    title = thread.name
    body = first_message.content

    # Check if there are any attachments in the message
    if first_message.attachments:
        attachments = "\n\n**Attachments:**\n" + "\n".join(
            [attachment.url for attachment in first_message.attachments]
        )
        body += attachments

    # Create the GitHub issue with the 'bug' label
    issue_url = bot.create_github_issue(title, body, [TAG_NAME])
    if issue_url:
        # Send the GitHub issue link in the thread
        # await thread.send(f"GitHub issue created: {issue_url}")
        await interaction.response.send_message(f"GitHub issue created: {issue_url}", ephemeral=False)
    else:
        await interaction.response.send_message("Failed to create GitHub issue.", ephemeral=True)

# Run the bot
bot.run(BOT_TOKEN)