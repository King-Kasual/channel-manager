from utils.sql import sql
from utils.create_channels import Create_Dynamic_Channels


def check_joined_channel(bot, db, debug=False):
    @bot.event
    async def on_voice_state_update(member, before, after):
        if after.channel is not None and (before.channel != after.channel):
            if debug:
                print(
                    f"{member.name} has joined {after.channel.name} ID: {after.channel.id}"
                )

            # Check if the channel joined is a static channel
            current_channels = sql.List_Channel_Static(db)
            if (after.channel.id.__str__() in current_channels) and (
                current_channels is not None
            ):
                if debug:
                    print(f"Channel {after.channel.name} is a static channel")
                new_channel_name = f"{member.name}'s {after.channel.name}"
                response = await Create_Dynamic_Channels(
                    member, after.channel, db, new_channel_name
                )
                if debug:
                    print(response)

        # Check if the channel left is a dynamic channel and if it is empty
        if before.channel is not None and (before.channel != after.channel):
            if debug:
                print(
                    f"{member.name} has left {before.channel.name} ID: {before.channel.id}"
                )
            current_channels = sql.List_Channel_Dynamic(db)
            if (before.channel.id.__str__() in current_channels) and (
                current_channels is not None
            ):
                if debug:
                    print(f"Channel {before.channel.name} is a dynamic channel")
                if len(before.channel.members) == 0:
                    from utils.delete_channels import Delete_Dynamic_Channels

                    response = await Delete_Dynamic_Channels(before.channel, db)
                    if debug:
                        print(response)
