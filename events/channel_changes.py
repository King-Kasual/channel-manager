from utils.sql import sql


def channel_changes(bot, db, debug):

    # Detect channel deletions in the guild and clean up DB entries
    @bot.event
    async def on_guild_channel_delete(channel):
        if sql.is_channel_Dynamic(db, channel.id.__str__(), debug):
            sql.Delete_channel_Dynamic(db, channel.id.__str__(), debug)
        if sql.is_Channel_Static(db, channel.id.__str__(), debug):
            sql.Delete_channel_Static(db, channel.id.__str__(), debug)
        if debug:
            print(f"A channel has been deleted: {channel.name}")

    # Detect channel updates (like name changes)
    @bot.event
    async def on_guild_channel_update(before, after):
        # Currently no DB fields to update, but log the event
        if debug:
            print(f"A channel has been updated from {before.name} to {after.name}")
