import discord
from utils.sql import sql


# Deletes static channels both from Discord and the database
async def Delete_Static_Channels(channel, db, debug=False):
    try:
        await channel.delete()
    except discord.Forbidden as e:
        response = f"Failed to delete channel {channel.name} due to permissions: {e}"
    except discord.HTTPException as e:
        response = f"Failed to delete channel {channel.name} due to HTTP error: {e}"
    else:
        sql.delete_channel(db, "channel_static", channel.id)
        response = f"Channel {channel.name} deleted successfully"

    if debug:
        print(response)
    return response


# Deletes dynamic channels both from Discord and the database
async def Delete_Dynamic_Channels(channel, db, debug=False):
    try:
        await channel.delete()
    except discord.Forbidden as e:
        response = f"Failed to delete channel {channel.name} due to permissions: {e}"
    except discord.HTTPException as e:
        response = f"Failed to delete channel {channel.name} due to HTTP error: {e}"
    else:
        sql.delete_channel(db, "channel_dynamic", channel.id)
        response = f"Channel {channel.name} deleted successfully"

    if debug:
        print(response)
    return response
