import discord
from discord.ext import commands
from utility import Config

class Guild(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conf = Config()
    
    @commands.Cog.listener(name="on_guild_join")
    async def on_guild_join(self, guild: discord.Guild):
        conf = self.conf.get()
        
        conf[str(guild.id)] = {}
        conf[str(guild.id)]["owner_id"] = guild.owner.id
        conf[str(guild.id)]["assigned_roles"] = {}
        
        self.conf.save(conf)
    
    @commands.Cog.listener(name="on_guild_remove")
    async def on_guild_remove(self, guild: discord.Guild):
        conf = self.conf.get()

        conf.pop(str(guild.id))
    
        self.conf.save(conf)

    
async def setup(bot):
    await bot.add_cog(Guild(bot))