import discord
from discord import app_commands
from constants import Roles
from utility import Config

def get_role_name(n: int):
    if n == 3:
        return "Owner"
    elif n == 2:
        return "Admin"
    elif n == 1:
        return "Mod"
    else:
        return "User"
    
def get_role_emoji(n: int):
    if n == 3:
        return ":crown:"
    elif n == 2:
        return ":wrench:"
    elif n == 1:
        return ":rotating_light:"
    else:
        return ""

def is_owner():
    def predicate(interaction: discord.Interaction) -> bool:
        
        conf = Config().get()
        level = 0
        if str(interaction.user.id) in conf[str(interaction.guild.id)]["assigned_roles"]:
            level = conf[str(interaction.guild.id)]["assigned_roles"][str(interaction.user.id)]
            
        if level >= Roles.Owner:
            return True
        return False
    return app_commands.check(predicate)

def is_admin():
    def predicate(interaction: discord.Interaction) -> bool:
        conf = Config().get()
        level = 0
        if str(interaction.user.id) in conf[str(interaction.guild.id)]["assigned_roles"]:
            level = conf[str(interaction.guild.id)]["assigned_roles"][str(interaction.user.id)]
            
        if level >= Roles.Administrator:
            return True
        return False
    return app_commands.check(predicate)

def is_mod():
    def predicate(interaction: discord.Interaction) -> bool:
        conf = Config().get()
        level = 0
        if str(interaction.user.id) in conf[str(interaction.guild.id)]["assigned_roles"]:
            level = conf[str(interaction.guild.id)]["assigned_roles"][str(interaction.user.id)]
            
        if level >= Roles.Moderator:
            return True
        return False
    return app_commands.check(predicate)