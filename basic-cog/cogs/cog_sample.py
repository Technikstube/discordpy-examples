"""
Sample Cog for the Basic Cog Setup

Author @SimplexDE
"""

import discord

from discord.ext import commands

class Ping(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    # A basic on_member_join Listener
    # Note that in cogs, all event listeners must be decorated with @commands.Cog.listener()
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        
        # Get the discord servers system channel
        channel = member.guild.system_channel
        
        # Send a welcome message to the channel, if it exists
        if channel is not None:
            await channel.send(f'Welcome {member.mention}.')


    # A basic prefix command
    @commands.command()
    async def ping(self, ctx: commands.Context):
        """Responds with 'Pong! 🏓'"""

        # Check if the command author is the bot, if true, cancel the command
        if ctx.author == self.bot.user:
            return
        
        # Reply to the command message
        await ctx.reply("Pong! 🏓")
        
        
    # A basic slash command
    @discord.app_commands.command(name="ping", description="Responds with 'Pong! 🏓'")
    async def ping_slash(self, interaction: discord.Interaction):
        """Responds with 'Pong! 🏓'"""
        
        # Sends the message as a reply to the command
        await interaction.response.send_message("Pong! 🏓")


# The setup function is necessary to load(aka register) the cog
# Read more: https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html#cog-registration
async def setup(bot):
    await bot.add_cog(Ping(bot))