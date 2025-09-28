import discord
from discord.ext import commands
from os import getenv
from dotenv import load_dotenv
import config

# --------------- LOAD ENVIROMENT VARIABLES ------------------
load_dotenv()
token, db_host, db_user, db_password, db_name, db_port = getenv('BOT_TOKEN_KEY', 'DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME', 'DB_PORT')

# --------------- SETUP DATABASE CONNECTION ------------------
db = config.DB_Connect(db_host, db_user, db_password, db_name, db_port)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# ---------------- IMPORT COMMANDS FUNCTIONS -----------------
from commands import create_channel
from commands import delete_channel
from commands import list_channels

# ----------------- CREATE COMMAND GROUPS --------------------
group = discord.app_commands.Group(name="channel_manager", description="Base Channel Manager Commmand")
group = create_channel.group_create(group, db)
group = delete_channel.group_delete(group, db)
group = list_channels.group_list(group, db)

bot.tree.add_command(group)

# ---------------- IMPORT EVENTS FUNCTIONS ------------------
from events import check_joined_channel

# ---------------------- RUN EVENTS -------------------------
check_joined_channel.check_joined_channel(bot)

    # Run the bot
if __name__ == "__main__":
    bot.run(token)