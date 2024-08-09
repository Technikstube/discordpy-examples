import discord

from discord.ext import commands
from discord import app_commands
from modal.ticket import TicketModal
from view.ticketopen import TicketOpenView
from utility import save_tickets, get_tickets

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="ticket", description="Open a Ticket")
    async def ticket_command(self, interaction: discord.Interaction):
        modal = TicketModal("Open a Ticket")
        await interaction.response.send_modal(modal)
    
    @app_commands.command(name="ticket_message", description="Send a Ticket-Creator Message")
    @app_commands.default_permissions(
        manage_guild=True
    )
    async def ticket_creator_command(self, interaction: discord.Interaction):
        
        embed = discord.Embed(
            title="Open a Ticket",
            description="Click on `Open Ticket` to create a Ticket",
            color=0x34e62e
        )
        
        await interaction.channel.send(embed=embed, view=TicketOpenView())
        await interaction.response.send_message("Created!", ephemeral=True)
        
    @app_commands.command(name="close", description="Close a Ticket")
    async def ticket_close_command(self, interaction: discord.Interaction):
        
        tickets = get_tickets()
        
        if str(interaction.channel.id) not in tickets:
            await interaction.response.send_message("This is not a ticket.", ephemeral=True)
            return
        
        tickets.pop(str(interaction.channel.id))
        save_tickets(tickets)
        
        await interaction.channel.delete()

async def setup(bot):
    await bot.add_cog(Tickets(bot))