import discord
from discord.ext import commands
from os import getenv
from dotenv import load_dotenv
import config
import asyncio


def main():

    # --------------- LOAD ENVIRONMENT VARIABLES ------------------
    load_dotenv()
    token = getenv("BOT_TOKEN_KEY")
    db_host = getenv("DB_HOST", "localhost")
    db_user = getenv("DB_USER", "chmgruser")
    db_password = getenv("DB_PASSWORD", "")
    db_name = getenv("DB_NAME", "channel-manager")
    db_port = int(getenv("DB_PORT", "5432"))
    debug = getenv("DEBUG", "False").lower() == "true"
    print(f"Debug Mode: {debug}")

    # --------------- SETUP DATABASE CONNECTION ------------------
    db = config.DB_Connect(db_host, db_user, db_password, db_name, db_port)

    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix="!", intents=intents)

    # ---------------- IMPORT COMMANDS FUNCTIONS -----------------
    from commands import create_channel
    from commands import delete_channel
    from commands import list_channels
    from commands import add_channel
    from commands import remove_channel 

    # ----------------- CREATE COMMAND GROUPS --------------------
    group = discord.app_commands.Group(
        name="channel_manager",
        description="Base Channel Manager Command",
        guild_only=True,
    )
    group = create_channel.group_create(bot, group, db, debug=debug)
    group = delete_channel.group_delete(group, db, debug=debug)
    group = list_channels.group_list(group, db, bot, debug=debug)
    group = add_channel.group_add_channel(group, db, bot, debug=debug)
    group = remove_channel.group_remove_channel(group, db, bot, debug=debug)

    bot.tree.add_command(group)

    # ---------------- IMPORT EVENTS FUNCTIONS ------------------
    from events import check_joined_channel
    from events import bot_on_ready
    from events import channel_changes

    # ---------------------- RUN EVENTS -------------------------
    check_joined_channel.check_joined_channel(bot, db, debug=debug)
    bot_on_ready.main_commands_sync(bot, db)
    channel_changes.channel_changes(bot, db, debug=debug)

    # ---------------------- START BOT --------------------------
    bot.run(token)


if __name__ == "__main__":
    main()
