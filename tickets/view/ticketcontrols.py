import discord
from discord import ui

class TicketControlsView(ui.View):
    def __init__(self, bot, channel: discord.TextChannel):
        super().__init__(timeout=0)
        self.bot = bot
        self.channel = channel
        
        self.close_button = ui.Button(
            label="Close Ticket", style=discord.ButtonStyle.red
        )
        
        self.add_item(self.close_button)
        
        self.close_button.callback = self.callback

    async def callback(self, interaction: discord.Interaction):
        
        # TODO: Implement function

        self.close_button.disabled = True
        self.stop()

    async def on_timeout(self):
        self.close_button.disabled = True
        self.stop()


def get_view(bot, channel: discord.TextChannel):
    return TicketControlsView(bot=bot, channel=channel)
