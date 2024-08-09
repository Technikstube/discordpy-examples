"""
A sample ticket bot

Author @SimplexDE
"""

import discord
import os
from discord.ext import commands
from dotenv import get_key
from view.ticketcontrols import TicketControlsView
from view.ticketopen import TicketOpenView

# If needed, change this to discord.Intents.all() and delete the two lines under it
# !IMPORTANT: This example bot needs the "Message Content" and "Server Members" intent
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

TOKEN = get_key(".env", "TOKEN")

class TicketBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents
        )

    async def setup_hook(self):
        """This makes sure that the Buttons are persistent, even after a bot restart."""
        
        self.add_view(TicketControlsView())
        self.add_view(TicketOpenView())
        
    async def on_ready(self):
        # go through the cogs folder
        for file in os.listdir("./tickets/cogs/"):
            
            # check if the file ends with ".py"
            if file.endswith(".py"):
                
                # if it ends with ".py", load it
                # FYI: "[:-3]" cuts off the ".py" (3 letters/symbols) at the end of the file name
                await self.load_extension(f"cogs.{file[:-3]}")
                print(f"Loaded Extension: {file[:-3]}")
                
        # Synchronize the slash commands to discord
        await self.tree.sync()
        
        print("Ready")
        
bot = TicketBot()
    
bot.run(TOKEN)
    
    