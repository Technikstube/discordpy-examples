import discord
from discord import utils
from discord.ext import commands
import asyncio

class MmSyt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.author.bot:
                return
            
            if isinstance(message.channel, discord.DMChannel):
                guild = self.bot.get_guild(12321231123) # Change the guild id to your guild id
                categ = utils.get(guild.categories, name = "Modmail Tickets") # Change to your Modmail category
                if not categ:
                    overwrites = {
                        guild.default_role: discord.PermissionOverwrite(read_messages = False),
                        guild.me : discord.PermissionOverwrite(read_messages = True)
                    }                                           
                    categ = await guild.create_category(name = "Modmail Tickets", overwrites = overwrites)

                channel = utils.get(categ.channels, topic = str(message.author.id))
                if not channel:
                    channel = await categ.create_text_channel(name = f"{message.author.name}", topic = str(message.author.id))
                    await channel.send(f"Neue Modmail Nachricht von {message.author.mention}") #Change "Neue Modmail Nachricht von" to your Message when user open a Ticket

                embed = discord.Embed(description = message.content, color = discord.Color.dark_green())
                embed.set_author(name = message.author)
                await channel.send(embed=embed)

            elif isinstance(message.channel, discord.TextChannel):
                if message.content.startswith(self.bot.command_prefix):
                    pass
                else:
                    topic = message.channel.topic
                    if topic:
                        member = message.guild.get_member(int(topic))
                        if member:
                            embed = discord.Embed(description= message.content, color = discord.Color.dark_green())     
                            embed.set_author(name = message.author)
                            await member.send(embed=embed)
        except Exception as e:
            print(e)

    @commands.command()
    async def close(self, ctx):
        if ctx.channel.category and ctx.channel.category.name == "Modmail Tickets": # Change to our Modmail tickets category
            await ctx.send("Ticket wird in 10 Sekunden gelöscht") # Change to your Delete Message
            await asyncio.sleep(10) # 10 Seconds to delete tickets. This can be changed later
            await ctx.channel.delete()

async def setup(bot):
    await bot.add_cog(MmSyt(bot))