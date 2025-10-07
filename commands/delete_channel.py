import discord



def group_delete(group, db):
    # Dispose of a channel flagged for automated channel creation
    @group.command(name="delete", description="Deletes an auto creating channel")
    async def delete(
        inter: discord.Interaction, channel: discord.abc.GuildChannel
    ) -> None:
    async def delete(
        inter: discord.Interaction, channel: discord.abc.GuildChannel
    ) -> None:
        await inter.response.send_message("")


    return group

