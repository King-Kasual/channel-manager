import discord
from discord import guild
import discord.channel
from utils.sql import sql


# Deletes static channels both from Discord and the database
async def Delete_Static_Channels(channel, db, debug=False):
    try:
        await channel.delete()
    except Exception as e:
        response = f"Failed to delete channel {channel.name} due to {e}"
    else:
        sql.Delete_channel_Static(db, channel.id)
        response = f"Channel {channel.name} deleted successfully"

    if debug:
        print(response)
    return response


# Deletes dynamic channels both from Discord and the database
async def Delete_Dynamic_Channels(channel, db, debug=False):
    try:
        await channel.delete()
    except Exception as e:
        response = f"Failed to delete channel {channel.name} due to {e}"
    else:
        sql.Delete_channel_Dynamic(db, channel.id)
        response = f"Channel {channel.name} deleted successfully"

    if debug:
        print(response)
    return response
