import discord
from utils.sql import sql

def group_remove_channel(group, db, bot, debug=False):
    # Remove a channel from being managed by bot
    @group.command(name="remove", description="Removes an auto creating channel")
    async def remove(inter: discord.Interaction, channel: discord.abc.GuildChannel) -> None:
        sql.delete_channel(db, "channel_static", channel.id, debug=debug)
        await inter.response.send_message(f"Channel '{channel.name}' removed from auto creating channels.")

    return group