import discord
from discord import guild
import discord.channel
from utils.sql import sql

# Creates new statuc channel to spawn dynamic channels off of
async def Create_Static_Channels(channel, db):

	new_channel = await channel.guild.create_voice_channel(name = channel,)

	sql.Add_channel_Static(db, new_channel.id)

	

# Creates new dynamic channel and move the member to the newly created channel
async def Create_Dynamic_Channels(member, channel):
  
	new_channel = await member.voice.channel.clone(name = channel)
 
	sql.Add_channel_Static(new_channel.id)
 
	await new_channel.set_permissions(
			member,
			manage_channels = True,
			move_members = True,
			priority_speaker = True,
			mute_members = True
	)
	await member.edit(voice_channel = new_channel)
