"""
A sample ticket bot

Author @SimplexDE
"""

import discord
import os
from discord.ext import commands

# If needed, change this to discord.Intents.all() and delete the two lines under it
# !IMPORTANT: This example bot needs the "Message Content" and "Server Members" intent
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

TOKEN = os.environ.get("TOKEN")

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    
    # go through the cogs folder
    for file in os.listdir("./basic-cog/cogs/"):
        
        # check if the file ends with ".py"
        if file.endswith(".py"):
            
            # if it ends with ".py", load it
            # FYI: "[:-3]" cuts off the ".py" (3 letters/symbols) at the end of the file name
            await bot.load_extension(f"cogs.{file[:-3]}")
            print(f"Loaded Extension: {file[:-3]}")
            
    # Synchronize the slash commands to discord
    await bot.tree.sync()
    
    print("Ready")
    
bot.run(TOKEN)
    
    