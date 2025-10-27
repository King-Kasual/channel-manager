from py_compile import main
from scripts import db_fix


def main_commands_sync(bot, db):

    # Sync the command tree when the bot is ready
    @bot.event
    async def on_ready():
        await bot.tree.sync()
        print("Bot is ready and commands are synced.")

        db_fix.fix_db_channel(db, bot)
