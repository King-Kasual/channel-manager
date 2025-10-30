import discord
from utils.sql import sql


def group_remove_channel(group, db, bot, debug=False):
    # Remove a channel from being managed by bot
    @group.command(name="remove", description="Removes an auto creating channel")
    async def remove(
        inter: discord.Interaction, channel: discord.abc.GuildChannel
    ) -> None:
        if inter.guild_id != channel.guild.id:
            await inter.response.send_message("Channel not in this guild")
            return
        if sql.channel_exists(db, "channel_dynamic", channel.id, debug):
            await inter.response.send_message(
                "Channel is a dynamic channel, and cannot be removed as static"
            )
            return
        if sql.channel_exists(db, "channel_static", channel.id, debug) is False:
            await inter.response.send_message("Channel not managed by bot")
            return
        sql.delete_channel(db, "channel_static", channel.id, debug=debug)
        await inter.response.send_message(
            f"Channel '{channel.name}' removed from auto creating channels."
        )

    return group
