import discord
from utils.sql import sql


def group_list(group, db, bot):
    # List channels managed by bot
    @group.command(name="list", description="Lists all auto creating channels")
    async def list(inter: discord.Interaction) -> None:

        channel_ID_list = sql.List_Channel_Static(db)
        inter.guild_id

        # This gets the ID list of channel that belond to the this guild
        channel_name_list = []
        for channel_ID in channel_ID_list:
            print(f"Channel_ID: {channel_ID}")
            channel = bot.get_channel(channel_ID)

            if channel.guild.id() == inter.guild_id():
                channel_name_list += channel.name()

        await inter.response.send_message(channel_name_list)

    return group
