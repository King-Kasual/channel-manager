def check_joined_channel(bot):
    @bot.event
    async def on_voice_state_update(member, before, after):
        if after.channel is not None and (before.channel != after.channel):
            print(f"{member.name} has joined {after.channel.name} ID: {after.channel.id}")