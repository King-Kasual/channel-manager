import discord
from discord import guild
import discord.channel
from utils.sql import sql


# Creates new static channel to spawn dynamic channels off of
async def Delete_Static_Channels(channel, db):
    try:
        await channel.delete()
    except Exception as e:
        response = f"Failed to delete channel {channel.name} due to {e}"
    else:
        sql.Delete_channel_Static(db, channel.id)
        response = f"Channel {channel.name} deleted successfully"

    print(response)
    return response


async def Delete_Dynamic_Channels(channel, db):
    try:
        await channel.delete()
    except Exception as e:
        response = f"Failed to delete channel {channel.name} due to {e}"
    else:
        sql.Delete_channel_Dynamic(db, channel.id)
        response = f"Channel {channel.name} deleted successfully"

    print(response)
    return response
