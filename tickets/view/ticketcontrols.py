import discord
from discord import ui
from utility import get_tickets, save_tickets

class TicketControlsView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
        self.close_button = ui.Button(
            label="Close Ticket", style=discord.ButtonStyle.red, custom_id="ticket_close"
        )
        
        self.add_item(self.close_button)
        
        self.close_button.callback = self.callback

    async def callback(self, interaction: discord.Interaction):
        tickets = get_tickets()
        tickets.pop(str(interaction.channel.id))
        save_tickets(tickets)
        
        await interaction.channel.delete()
