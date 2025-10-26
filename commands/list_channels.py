import discord
from utils.sql import sql


def group_list(group, db, bot, debug=False):
    # List channels managed by bot
    @group.command(name="list", description="Lists all auto creating channels")
    async def list(inter: discord.Interaction) -> None:
        channel_name_list = sql.list_channel_name(db, "channel_static", debug=debug)
        await inter.response.send_message(channel_name_list)

    return group
