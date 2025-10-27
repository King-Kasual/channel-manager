from utils.sql import sql
from utils.create_channels import Create_Dynamic_Channels
from utils.delete_channels import Delete_Dynamic_Channels


def check_joined_channel(bot, db, debug=False):
    @bot.event
    async def on_voice_state_update(member, before, after):
        if after.channel is not None and (before.channel != after.channel):
            if debug:
                print(
                    f"{member.display_name} has joined {after.channel.name} ID: {after.channel.id}"
                )

            # Check if the channel joined is a static channel
            if sql.channel_exists(db, "channel_static", after.channel.id, debug):
                if debug:
                    print(f"Channel {after.channel.name} is a static channel")
                new_channel_name = f"{member.display_name}'s {after.channel.name}"
                length = len(new_channel_name)
                if length > 100:
                    new_channel_name = new_channel_name[:100]
                response = await Create_Dynamic_Channels(
                    bot, member, after.channel, db, new_channel_name
                )
                if debug:
                    print(response)

        # Check if the channel left is a dynamic channel and if it is empty
        if before.channel is not None and (before.channel != after.channel):
            if debug:
                print(
                    f"{member.display_name} has left {before.channel.name} ID: {before.channel.id}"
                )
            if sql.channel_exists(db, "channel_dynamic", before.channel.id, debug):
                if debug:
                    print(f"Channel {before.channel.name} is a dynamic channel")
                if len(before.channel.members) == 0:
                    response = await Delete_Dynamic_Channels(before.channel, db)
                    if debug:
                        print(response)
