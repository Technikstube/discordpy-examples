import discord
from discord import utils
from discord.ext import commands
import asyncio
import json

SERVERGUILD = 1226865662224240671  # Change the guild id to your guild id
TICKETCATEG = 1271451509015449600 # Change the ticket id to your ticket id

# Pfad zur JSON-Datei
TICKETS_FILE = 'tickets.json'

def load_tickets():
    try:
        with open(TICKETS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"ticket_channels": {}}

def save_tickets(tickets_data):
    with open(TICKETS_FILE, 'w') as file:
        json.dump(tickets_data, file, indent=4)

class ModmailSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
                return
            
        if isinstance(message.channel, discord.DMChannel):
            guild = self.bot.get_guild(SERVERGUILD)
            categ = utils.get(guild.categories, id=TICKETCATEG)

            channel = utils.get(categ.text_channels, topic=str(message.author.id))
            if not channel:
                channel = await categ.create_text_channel(name = f"{message.author.name}", topic = str(message.author.id))

                # Save the Channel as Ticket Channel
                tickets_data = load_tickets()
                tickets_data["ticket_channels"][str(channel.id)] = {"topic": str(message.author.id)}
                save_tickets(tickets_data)

                await channel.send(f"Neue Modmail Nachricht von {message.author.mention}")

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


    @commands.command()
    async def close(self, ctx):
        tickets_data = load_tickets()
        if str(ctx.channel.id) in tickets_data["ticket_channels"]:
            await ctx.send("Ticket wird in 10 Sekunden gelöscht")
            await asyncio.sleep(10) # 10 Sekunden, um das Ticket zu löschen. Dies kann später geändert werden.
            
            #Delete the Ticket Channel from JSON File
            if str(ctx.channel.id) in tickets_data["ticket_channels"]:
                del tickets_data["ticket_channels"][str(ctx.channel.id)]
                save_tickets(tickets_data)

            await ctx.channel.delete()
        else:
            await ctx.send("Dies ist keine Modmail-Ticket-Kanal!")


async def setup(bot):
    await bot.add_cog(ModmailSystem(bot))