import discord
from discord import ui


class TicketModal(ui.Modal):
    def __init__(self, title: str):
        super().__init__(title=title)
        self.reason = ui.TextInput(
            label="Reason",
            style=discord.TextStyle.short,
            required=True,
            placeholder="...",
        )

        self.add_item(self.reason)

    async def on_submit(self, interaction: discord.Interaction):
        
        # TODO: Implement function
        
        self.stop()
