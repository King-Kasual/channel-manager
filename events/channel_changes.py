from utils.sql import sql


def channel_changes(bot, db, debug):

    # Detect channel deletions in the guild and clean up DB entries
    @bot.event
    async def on_guild_channel_delete(channel):
        if sql.channel_exists(db, "channel_dynamic", channel.id, debug):
            sql.delete_channel(db, "channel_dynamic", channel.id, debug)
        if sql.channel_exists(db, "channel_static", channel.id, debug):
            sql.delete_channel(db, "channel_static", channel.id, debug)
        if debug:
            print(f"A channel has been deleted: {channel.name}")

    # Detect channel updates (like name changes)
    @bot.event
    async def on_guild_channel_update(before, after):
        if sql.channel_exists(db, "channel_dynamic", before.id, debug):
            sql.update_channel_name(db, "channel_dynamic", after.id, after.name, debug)
        if sql.channel_exists(db, "channel_static", before.id, debug):
            sql.update_channel_name(db, "channel_static", after.id, after.name, debug)
        if debug:
            print(f"A channel has been updated from {before.name} to {after.name}")
