from py_compile import main


def main_commands_sync(bot):

    # Sync the command tree when the bot is ready
    @bot.event
    async def on_ready():
        await bot.tree.sync()
        print("Bot is ready and commands are synced.")
