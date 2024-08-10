import discord
import datetime
from typing import Optional
from discord.ext import commands
from discord import app_commands
from check import is_admin, is_mod, is_owner

class ExampleModeration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="ban", description="Ban a member.")
    @is_owner()
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: Optional[str]=None):
        await interaction.guild.ban(member, delete_message_days=0, reason=reason)
        await interaction.response.send_message(f"{member.mention} was banned!", ephemeral=True)

    @app_commands.command(name="unban", description="Pardon a member.")
    @is_admin()
    async def unban(self, interaction: discord.Interaction, member: discord.User, reason: Optional[str]=None):
        await interaction.guild.unban(member, reason=reason)
        await interaction.response.send_message(f"{member.mention} was unbanned!", ephemeral=True)

    @app_commands.command(name="kick", description="Kick a member.")
    @is_admin()
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: Optional[str]=None):
        await interaction.guild.kick(member, reason=reason)
        await interaction.response.send_message(f"{member.mention} was kicked!", ephemeral=True)


    @app_commands.command(name="timeout", description="Timeout a member.")
    @is_mod()
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, duration: str, reason: Optional[str]=None):
        until = datetime.timedelta(hours=1)
        
        if duration.endswith("s"):
            until = datetime.timedelta(seconds=int(duration[:-1]))
        elif duration.endswith("m"):
            until = datetime.timedelta(minutes=int(duration[:-1]))
        elif duration.endswith("h"):
            until = datetime.timedelta(hours=int(duration[:-1]))
        elif duration.endswith("d"):
            until = datetime.timedelta(days=int(duration[:-1]))
    
        await member.timeout(until, reason=reason)
        await interaction.response.send_message(f"{member.mention} was timeouted for {duration}.", ephemeral=True)

    @app_commands.command(name="untimeout", description="Remove a timeout from a member.")
    @is_mod()
    async def untimeout(self, interaction: discord.Interaction, member: discord.Member, reason: Optional[str]=None):
        await member.timeout(None, reason=reason)
        await interaction.response.send_message(f"{member.mention}'s timeout was removed.", ephemeral=True)

    async def cog_app_command_error(self, interaction: discord.Interaction, error: Exception):
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("You dont have the Permission to do that.", ephemeral=True)
        elif isinstance(error, discord.Forbidden):
            await interaction.response.send_message("I dont have permission to do that!", ephemeral=True)
        else:
            await interaction.response.send_message("Something went wrong!", ephemeral=True)
            raise error
    
async def setup(bot):
    await bot.add_cog(ExampleModeration(bot))