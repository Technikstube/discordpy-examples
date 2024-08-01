"""
A slash command for calculating the ping in milliseconds and returning it to the user.

Author @SimplexDE
"""

import discord
from discord.ext.commands import Bot

# Insert your Bot-Token here
TOKEN = "bot_token_here"

# If needed, change this to discord.Intents.all() to enable all intents. The ping slash command works with default.
intents = discord.Intents.default()

bot = Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    
    # Syncronize the slash commands to discord
    await bot.tree.sync()
    
    print("Ready!")

@bot.tree.command(name="ping", description="Shows the current latency")
async def ping_slash_command(interaction: discord.Interaction):
    """The ping slash command

    Args:
        interaction (discord.Interaction): The interaction
    """
        
    # Takes the latency and multiplies it with 1000 to make it milliseconds
    # Rounding is for readability
    latency = round(bot.latency * 1000)

    # Sends the message as a reply to the command
    await interaction.response.send_message(f"{bot.user.name}'s Ping is: {latency}ms")
    

# Run the bot with the set TOKEN
bot.run(TOKEN)