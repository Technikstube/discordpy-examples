"""
A sample temporary voice channel bot

Author @SimplexDE
"""

import discord
from discord.ext import commands


# If needed, change this to discord.Intents.all(). This example works with default.
intents = discord.Intents.default()

# Set your Bot-Token here
TOKEN = "bot_token_here"

# This list is used to temporarily save the created channels for later removal
channels = []

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():  
    print("Ready")
    
# The "on_voice_state_update" event checks if any member in any guild joins any voice channel
# API Reference: https://discordpy.readthedocs.io/en/stable/api.html?highlight=on_voice#discord.on_voice_state_update
@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
      
    # Add your "Create Channel"-Voicechannel id here
    create_channel_id =  0000000000000000000

    # Add your desired voice category id here
    # If set to None, the category of the creator channel is used.
    category_id = None  
    
    if category_id is None:
        
        # Get the create channel
        _chn = bot.get_channel(create_channel_id)
        
        # Checks if the channel exists
        if _chn is None:
            print("The create channel was not found, did you copy the right id?")
        
        # Sets the category_id to the create channels category id
        category_id = _chn.category_id
    
    if after.channel:
        if after.channel.id == create_channel_id:
            
            # Create the temporary voice channel if a user joins into the creator channel
            created_voice_channel = await after.channel.guild.create_voice_channel(
                name=f"{member.name}'s Talk", 
                reason="Temp-Voice Channel created", 
                category=bot.get_channel(category_id) 
                )
            
            # Moves the member to the newly created voice channel
            await member.move_to(
                created_voice_channel,
                reason="Moved to Temp-Voice channel"
                )
            
            # Adds the channel id to the channels list for later removal
            channels.append(created_voice_channel.id)
    
    
    if before.channel:    
        if before.channel.id in channels:
            
            # Checks if there are no more users in the voice channel
            if len(before.channel.members) == 0:
                
                # Deletes the voice channel
                await before.channel.delete(reason="Temp-Voice channel empty")
                
                # Remove the id out of the channels list
                channels.remove(before.channel.id)

bot.run(TOKEN)