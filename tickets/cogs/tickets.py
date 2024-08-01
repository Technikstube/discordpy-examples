import discord

from typing import Optional
from discord.ext import commands
from discord import app_commands

class Tickets(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="ticket", description="Open a Ticket")
    async def ticket_command(self, interaction: discord.Interaction, reason: Optional[str]="Nicht angegeben"):
        ...

async def setup(bot):
    await bot.add_cog(Tickets(bot))