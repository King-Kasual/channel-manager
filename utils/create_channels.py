import discord
from discord import PermissionOverwrite
from utils.sql import sql
from utils.delete_channels import Delete_Dynamic_Channels


# Creates new static channel to spawn dynamic channels off of
async def Create_Static_Channels(
    bot, name, channel, db, debug=False
):  # pylint: disable=too-many-arguments,too-many-positional-arguments
    try:
        new_channel = await channel.guild.create_voice_channel(
            name=name,
            overwrites={
                bot.user: PermissionOverwrite(
                    manage_permissions=True, move_members=True
                )
            },
            category=channel,
        )
    except discord.Forbidden as e:
        print(f"The bot is missing the permission: {e}")
        return PermissionError(f"Permission error: {e}")
    except discord.HTTPException as e:
        print(f"Creating channel {name} failed due to {e}")
        return ConnectionError(f"HTTP error: {e}")
    except discord.InvalidArgument as e:
        print(f"Invalid argument provided: {e}")
        return ValueError(f"Invalid argument: {e}")
    sql.add_channel(db, "channel_static", new_channel.id, name, new_channel.guild.id)
    if debug:
        print(f"Channel {name} created successfully")
    return new_channel


# Creates new dynamic channel and move the member to the newly created channel
async def Create_Dynamic_Channels(
    bot, member, channel, db, name, debug=False
):  # pylint: disable=too-many-arguments,too-many-positional-arguments,too-many-return-statements
    try:
        new_channel = await member.voice.channel.clone(
            name=name, category=channel.category
        )
    except discord.InvalidArgument as e:
        print(f"Invalid argument provided: {e}")
        return ValueError(f"Invalid argument: {e}")
    except discord.Forbidden as e:
        print(f"The bot is missing the permission: {e}")
        return PermissionError(f"Permission error: {e}")
    except discord.HTTPException as e:
        print(f"Creating channel {name} failed due to {e}")
        return ConnectionError(f"HTTP error: {e}")
    sql.add_channel(db, "channel_dynamic", new_channel.id, name, new_channel.guild.id)
    if debug:
        print(f"Channel {member.name} created successfully")

    # Set permissions for the new channel
    try:
        await new_channel.edit(
            overwrites={
                bot.user: PermissionOverwrite(
                    manage_permissions=True, move_members=True
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
        )
    except discord.Forbidden as e:
        print(f"The bot is missing the permission: {e}")
        await Delete_Dynamic_Channels(new_channel, db, debug=debug)
        return PermissionError(f"Permission error: {e}")
    except discord.HTTPException as e:
        print(f"Setting permissions for channel {name} failed due to {e}")
        await Delete_Dynamic_Channels(new_channel, db, debug=debug)
        return ConnectionError(f"HTTP error: {e}")
    if debug:
        print(f"Permissions for channel {name} set successfully")

    # Move member to the newly created channel
    try:
        await member.edit(voice_channel=new_channel)
    except discord.Forbidden as e:
        print(f"The bot is missing the permission: {e}")
        await Delete_Dynamic_Channels(new_channel, db, debug=debug)
        return PermissionError(f"Permission error: {e}")
    except discord.HTTPException as e:
        print(f"Moving member {member.name} to channel {name} failed due to {e}")
        await Delete_Dynamic_Channels(new_channel, db, debug=debug)
        return ConnectionError(f"HTTP error: {e}")
    if debug:
        print(f"Member {member.name} moved to channel {name} successfully")

    return new_channel
