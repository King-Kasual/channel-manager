import discord
from utils.sql import sql


def group_add_channel(group, db, bot, debug=False):
    # Add a new channel to be managed by bot
    @group.command(name="add", description="Adds a new auto creating channel")
    async def add(
        inter: discord.Interaction, channel: discord.abc.GuildChannel
    ) -> None:
        result = sql.add_channel(
            db,
            "channel_static",
            channel.id,
            channel.name,
            channel.guild.id,
            debug=debug,
        )
        await inter.response.send_message(
            f"Channel '{channel.name}' added to auto creating channels."
        )

    return group
