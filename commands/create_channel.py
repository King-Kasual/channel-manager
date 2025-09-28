import discord
from discord.ext import commands
from utils.sql import sql


def group_create(group):
    # Create a command should "flag" a voice channel, so when a user enters the channel it runs an event to create a new channel "owned" by the user who joined
    @group.command(name="create", description="Creates an auto creating channel")
    async def create(inter: discord.Interaction, name: str, channel: discord.abc.GuildChannel) -> None:
        sql.Add_channel_Static
        # await commands.create_channel(name,channel)
        await inter.response.send_message(f"{name}")
        
    return group