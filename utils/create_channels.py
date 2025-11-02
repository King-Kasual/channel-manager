import discord
from discord import PermissionOverwrite
from utils.sql import sql


# Creates new static channel to spawn dynamic channels off of
async def Create_Static_Channels(  # pylint: disable=too-many-arguments,too-many-positional-arguments
    bot, name, channel, db, debug=False
):
    try:
        new_channel = await channel.guild.create_voice_channel(
            name=name,
            overwrites={
                bot.user: PermissionOverwrite(
                    manage_permissions=True,
                    move_members=True,
                )
            },
            category=channel,
        )

    except discord.Forbidden as e:
        response = f"The bot is missing the permission: {e}"
        print(response)
    except discord.HTTPException as e:
        response = f"Failed to create channel {name} due to {e}"
        print(response)
    else:
        sql.add_channel(
            db, "channel_static", new_channel.id, name, new_channel.guild.id
        )
        response = f"Channel {name} created successfully"
    if debug:
        print(response)
    return response


# Creates new dynamic channel and move the member to the newly created channel
async def Create_Dynamic_Channels(  # pylint: disable=too-many-arguments,too-many-positional-arguments
    bot, member, channel, db, name, debug=False
):
    try:
        new_channel = await channel.guild.create_voice_channel(
            name=name,
            overwrites={
                bot.user: PermissionOverwrite(
                    manage_permissions=True,
                    move_members=True,
                ),
                member: PermissionOverwrite(
                    manage_channels=True,
                    move_members=True,
                    priority_speaker=True,
                    mute_members=True,
                    deafen_members=True,
                    view_channel=True,
                    connect=True,
                    speak=True,
                    stream=True,
                    use_voice_activation=True,
                    manage_permissions=True,
                    manage_messages=True,
                    read_message_history=True,
                    send_messages=True,
                    send_tts_messages=True,
                    embed_links=True,
                    attach_files=True,
                    read_messages=True,
                ),
            },
            category=channel.category,
            user_limit=channel.user_limit,
        )
        await member.edit(voice_channel=new_channel)
    except discord.Forbidden as e:
        response = f"The bot is missing the permission: {e}"
        print(response)
    except discord.HTTPException as e:
        response = f"Failed to create channel {name} due to {e}"
        print(response)
    else:
        sql.add_channel(
            db, "channel_dynamic", new_channel.id, name, new_channel.guild.id
        )
        response = f"Channel {member.name} created successfully"
    if debug:
        print(response)
    return response
