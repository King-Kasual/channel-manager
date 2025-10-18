import discord
from discord.ext import commands
from utils.create_channels import Create_Static_Channels


def group_create(group, db, debug=False):
    # Create a command should "flag" a voice channel, so when a user enters the channel it runs an event to create a new channel "owned" by the user who joined
    @group.command(name="create", description="Creates an auto creating channel")
    async def create(
        inter: discord.Interaction, name: str, channel: discord.abc.GuildChannel
    ) -> None:
        response = await Create_Static_Channels(name, channel, db, debug=debug)
        await inter.response.send_message(response)

    return group
