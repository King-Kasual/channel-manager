import discord
from discord import guild
import discord.channel
from utils.sql import sql


# Creates new static channel to spawn dynamic channels off of
async def Create_Static_Channels(name, channel, db, debug=False):
    try:
        new_channel = await channel.guild.create_voice_channel(
            name=name, category=channel
        )
    except Exception as e:
        response = f"Failed to create channel {name} due to {e}"
    else:
        sql.add_channel(
            db, "channel_static", new_channel.id, name, new_channel.guild.id
        )
        response = f"Channel {name} created successfully"
    if debug:
        print(response)
    return response


# Creates new dynamic channel and move the member to the newly created channel
async def Create_Dynamic_Channels(member, channel, db, name, debug=False):

    try:
        new_channel = await member.voice.channel.clone(
            name=name, category=channel.category
        )
        await new_channel.set_permissions(
            member,
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
        )
        await member.edit(voice_channel=new_channel)
    except Exception as e:
        response = f"Failed to create channel {member.name} due to {e}"
    else:
        sql.add_channel(
            db, "channel_dynamic", new_channel.id, name, new_channel.guild.id
        )
        response = f"Channel {member.name} created successfully"
    if debug:
        print(response)
    return response
