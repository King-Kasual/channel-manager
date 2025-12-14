import discord
from utils.create_channels import Create_Static_Channels


def group_create(bot, group, db, debug=False):
    # Create a command to "flag" a voice channel. When a user enters the
    # channel it triggers an event to create a new channel "owned" by the
    # user who joined.
    @group.command(name="create", description="Creates an auto creating channel")
    async def create(
        inter: discord.Interaction, name: str, channel: discord.abc.GuildChannel
    ) -> None:
        response = await Create_Static_Channels(bot, name, channel, db, debug=debug)
        await inter.response.send_message(response)

    return group
