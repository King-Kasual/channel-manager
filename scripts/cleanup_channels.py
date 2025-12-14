from utils.sql import sql
from utils.delete_channels import Delete_Dynamic_Channels


async def cleanup_static_channels(db, bot, debug=False):
    """Cleans up static channels that no longer exist in the database."""
    channels = sql.list_channel_id(db, "channel_static", debug=debug)
    for channel in channels:
        channel_id = channel
        if bot.get_channel(channel_id) is None:
            if debug:
                print(f"Cleaning up static channel ID: {channel_id}")
            sql.delete_channel(db, "channel_static", channel_id, debug=debug)


async def cleanup_dynamic_channels(db, bot, debug=False):
    """Cleans up dynamic channels that no longer exist in the database."""
    channels = sql.list_channel_id(db, "channel_dynamic", debug=debug)
    for channel in channels:
        channel_id = channel
        if bot.get_channel(channel_id) is None:
            if debug:
                print(f"Cleaning up dynamic channel ID: {channel_id}")
            sql.delete_channel(db, "channel_dynamic", channel_id, debug=debug)
        elif bot.get_channel(channel_id).members == []:
            if debug:
                print(f"Cleaning up empty dynamic channel ID: {channel_id}")
            sql.delete_channel(db, "channel_dynamic", channel_id, debug=debug)
            await Delete_Dynamic_Channels(bot.get_channel(channel_id), db, debug=debug)
