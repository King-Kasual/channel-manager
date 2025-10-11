import discord
from discord.ext import commands
from os import getenv
from dotenv import load_dotenv
import config


def main():

    # --------------- LOAD ENVIRONMENT VARIABLES ------------------
    load_dotenv()
    token = getenv("BOT_TOKEN_KEY")
    db_host = getenv("DB_HOST", "localhost")
    db_user = getenv("DB_USER", "chmgruser")
    db_password = getenv("DB_PASSWORD", "")
    db_name = getenv("DB_NAME", "channel-manager")
    db_port = int(getenv("DB_PORT", "5432"))

    # --------------- SETUP DATABASE CONNECTION ------------------
    db = config.DB_Connect(db_host, db_user, db_password, db_name, db_port)

    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix="!", intents=intents)

    # ---------------- IMPORT COMMANDS FUNCTIONS -----------------
    from commands import create_channel
    from commands import delete_channel
    from commands import list_channels

    # ----------------- CREATE COMMAND GROUPS --------------------
    group = discord.app_commands.Group(
        name="channel_manager", description="Base Channel Manager Commmand"
    )
    group = discord.app_commands.Group(
        name="channel_manager", description="Base Channel Manager Commmand"
    )
    group = create_channel.group_create(group, db)
    group = delete_channel.group_delete(group, db)
    group = list_channels.group_list(group, db, bot)

    bot.tree.add_command(group)

    # ---------------- IMPORT EVENTS FUNCTIONS ------------------
    from events import check_joined_channel

    # ---------------------- RUN EVENTS -------------------------
    check_joined_channel.check_joined_channel(bot, db)

    # Run the bot
    bot.run(token)


if __name__ == "__main__":
    main()
