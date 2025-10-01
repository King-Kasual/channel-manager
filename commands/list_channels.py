import discord

def group_list(group, db):
    # List channels managed by bot
    @group.command(name="list", description="Lists all auto creating channels")
    async def list(inter: discord.Interaction) -> None:
        await inter.response.send_message("")
        
    return group
