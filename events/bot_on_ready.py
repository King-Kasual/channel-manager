from py_compile import main
from scripts import db_fix, cleanup_channels


def main_commands_sync(bot, db):

    # Sync the command tree when the bot is ready
    @bot.event
    async def on_ready():
        await bot.tree.sync()
        print("Bot is ready and commands are synced.")

        db_fix.fix_db_channel(db, bot)
        await cleanup_channels.cleanup_static_channels(db, bot)
        await cleanup_channels.cleanup_dynamic_channels(db, bot)
        print("Database channels cleaned up.")
