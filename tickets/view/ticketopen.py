import discord
from discord import ui
from modal.ticket import TicketModal

# Class to add the Open Ticket Button

class TicketOpenView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
        self.open_button = ui.Button(
            label="Open Ticket", style=discord.ButtonStyle.green, custom_id="ticket_open"
        )
        
        self.add_item(self.open_button)
        
        self.open_button.callback = self.callback

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(TicketModal("Open a Ticket"))
