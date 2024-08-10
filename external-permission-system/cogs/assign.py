import discord

from discord.ext import commands
from discord import app_commands
from constants import Roles
from utility import Config
from check import get_role_name, get_role_emoji, is_mod

options: list = [
    app_commands.Choice(name="Owner (autom. assigned)", value=Roles.Owner),
    app_commands.Choice(name="Administrator", value=Roles.Administrator),
    app_commands.Choice(name="Moderator", value=Roles.Moderator),
    app_commands.Choice(name="User", value=Roles.User),
]

class Manage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conf = Config()
    
    @app_commands.command(name="assign", description="Assign a Role")
    @app_commands.choices(role=options)
    @is_mod()
    async def assign_command(self, interaction: discord.Interaction, member: discord.Member, role: app_commands.Choice[int]):
        conf = self.conf.get()

        executor_level = 0
        if str(interaction.user.id) in conf[str(interaction.guild.id)]["assigned_roles"]:
            executor_level = conf[str(interaction.guild.id)]["assigned_roles"][str(interaction.user.id)]
        
        target_level = 0
        if str(member.id) in conf[str(interaction.guild.id)]["assigned_roles"]:
            target_level = conf[str(interaction.guild.id)]["assigned_roles"][str(member.id)]
        
        if interaction.user == member:
            await interaction.response.send_message("You cannot assign yourself a new role.", ephemeral=True)
            return
        
        if executor_level <= role.value:
            await interaction.response.send_message(f"Your rank (`{get_role_name(executor_level)}`) isn't high enough to assign `{get_role_name(role.value)}`", ephemeral=True)
            return
        
        if target_level >= executor_level:
            await interaction.response.send_message(f"Your rank (`{get_role_name(executor_level)}`) is below `{get_role_name(target_level)}`, therefore you can't assign any rank to {member.mention}.", ephemeral=True)
            return
        
        if target_level == role.value:
            await interaction.response.send_message(f"{member.mention} is already assigned to `{get_role_name(role.value)}`.", ephemeral=True)
            return

        conf[str(interaction.guild.id)]["assigned_roles"][str(member.id)] = role.value
        self.conf.save(conf)
        
        await interaction.response.send_message(f"You've assigned {member.mention} to {role.name}", ephemeral=True)
    
    @assign_command.error
    async def assign_error(self, interaction: discord.Interaction, error: Exception):
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("You dont have the Permission to do that.", ephemeral=True)
        else:
            await interaction.response.send_message("Something went wrong!", ephemeral=True)
    
    @app_commands.command(name="userinfo", description="Show some Info about a user")
    async def userinfo_command(self, interaction: discord.Interaction, member: discord.Member):
        
        conf = self.conf.get()
        level = 0
        if str(member.id) in conf[str(interaction.guild.id)]["assigned_roles"]:
            level = conf[str(interaction.guild.id)]["assigned_roles"][str(member.id)]
        
        embed = discord.Embed(
            title=f"About {member.name}{get_role_emoji(level)}",
            description=""
        )
        embed.add_field(name="Permissionlevel:", value=f"{get_role_name(level)}{get_role_emoji(level)}")
        
        await interaction.response.send_message(embed=embed)
    
async def setup(bot):
    await bot.add_cog(Manage(bot))