import discord
from utility import get_tickets, save_tickets
from discord import ui
from view.ticketcontrols import TicketControlsView

# Set your Ticket-Category here, or None
CATEGORY_ID = None

class TicketModal(ui.Modal):
    def __init__(self, title: str):
        super().__init__(title=title, timeout=300) # Timeout 300 seconds = 5 minutes
        self.reason = ui.TextInput(
            label="Reason",
            style=discord.TextStyle.short,
            required=True,
            placeholder="Reason for opening the Ticket",
        )

        self.add_item(self.reason)

    # This is called when you click on Submit in the modal
    async def on_submit(self, interaction: discord.Interaction):
        
        category = interaction.guild.get_channel(CATEGORY_ID)
        guild = interaction.guild
        user = interaction.user
        
        channel = await guild.create_text_channel(
            name=f"{user.name}-ticket",
            reason=self.reason.value,
            category=category
            )

        embed = discord.Embed(
            title=f"Ticket from {user.name}",
            description=f"**Reason:** {self.reason.value}"
            )
        
        # Save the channel to tickets.json
        tickets = get_tickets()
        tickets[channel.id] = {}
        tickets[channel.id]["owner-id"] = user.id
        save_tickets(tickets)
        
        await channel.send(f"{user.mention}", embed=embed, view=TicketControlsView())
        await interaction.response.send_message(f"{channel.mention} was created...", ephemeral=True)
        self.stop()
        
    async def on_timeout(self, interaction: discord.Interaction):
        await interaction.response.send_message("Timeout... You took too long, please try again!", ephemeral=True)
        self.stop()