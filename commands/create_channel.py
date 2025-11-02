import discord
from utils.create_channels import Create_Static_Channels


def group_create(bot, group, db, debug=False):
    # Flag a voice channel so joining users get their own dynamic channel.
    @group.command(name="create", description="Creates an auto creating channel")
    async def create(
        inter: discord.Interaction, name: str, channel: discord.abc.GuildChannel
    ) -> None:
        response = await Create_Static_Channels(bot, name, channel, db, debug=debug)
        await inter.response.send_message(response)

    return group
