import discord
from utils.delete_channels import Delete_Static_Channels
from utils.sql import sql


def group_delete(group, db, debug=False):
    # Dispose of a channel flagged for automated channel creation
    @group.command(name="delete", description="Deletes an auto creating channel")
    async def delete(
        inter: discord.Interaction, channel: discord.abc.GuildChannel
    ) -> None:
        if inter.guild_id != channel.guild.id:
            await inter.response.send_message("Channel not in this guild")
            return
        if sql.channel_exists(db, "channel_static", channel.id, debug) is False:
            await inter.response.send_message("Channel not managed by bot")
            return
        response = await Delete_Static_Channels(channel, db, debug=debug)
        await inter.response.send_message(response)

    return group
