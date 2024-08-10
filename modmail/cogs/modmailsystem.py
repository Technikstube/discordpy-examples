import discord
from discord import utils
from discord.ext import commands
import asyncio
import json
import os

SERVERGUILD = 1224376462224240671 # Change to your Discord Guild ID
TICKETCATEG = 1271423509015449600 # Change to your Discord Modmail Category ID
TEAMROLE = 1261744325221349459 # Change to your Support oder Team Role ID

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
            role = guild.get_role(TEAMROLE)

            if not channel:
                channel = await categ.create_text_channel(name = f"{message.author.name}", topic = str(message.author.id))

                tickets_data = load_tickets()
                tickets_data["ticket_channels"][str(channel.id)] = {"id": str(message.author.id)}
                save_tickets(tickets_data)

                await channel.send(f"{role.mention}", delete_after = 3.0)

            embed = discord.Embed(description = message.content, color = 0x245400) # Change the Color to your favorite color
            embed.set_author(name = "📨 Neue Nachricht") # You can edit "📨 Neue Nachricht" to your Message
            embed.set_footer(text= f"Gesendet von {message.author}") # You can edit "Gesendet von" to your Message
            await channel.send(embed=embed)

        elif isinstance(message.channel, discord.TextChannel):
            if message.content.startswith(self.bot.command_prefix):
                return
            tickets_data = load_tickets()
            if str(message.channel.id) in tickets_data["ticket_channels"]:
                member_id = tickets_data["ticket_channels"][str(message.channel.id)].get("id")
                member = message.guild.get_member(int(member_id))
                embed = discord.Embed(description = message.content, color=0x245400)  # Change the Color to your favorite color 
                embed.set_author(name="📨 Reply from the Support Team")  # You can edit "📨 Reply from the Support Team" to your Message
                embed.set_footer(text=f"Sent by {message.author} from {message.guild.name}")  # You can edit "Sent by {message.author} from {message.guild.name" to your Message
                await member.send(embed=embed)


    @commands.command()
    async def close(self, ctx):
        tickets_data = load_tickets()
        if str(ctx.channel.id) in tickets_data["ticket_channels"]:

            embed = discord.Embed(description=f"❌ The ticket has been closed and will be deleted in 10 seconds!", color=0x245400) # You can edit "❌ The ticket has been closed and will be deleted in 10 seconds!" to your Message, and the Color to your favorite Color
            await ctx.send(embed=embed)

            # Collect als Messages in the Ticket
            messages = []
            async for message in ctx.channel.history(limit=None, oldest_first=True):
                messages.append(message)

            # Create Transcript
            transcript = f"Transcript von {ctx.channel.name}\n"
            for msg in messages:
                transcript += f"{msg.created_at} - {msg.author}: {msg.content}\n"

            # Write the transcript in a text file
            filename = f"transcript_{ctx.channel.name}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(transcript)

            await asyncio.sleep(10)
            
            if str(ctx.channel.id) in tickets_data["ticket_channels"]:
                del tickets_data["ticket_channels"][str(ctx.channel.id)]
                save_tickets(tickets_data)
            
            await ctx.channel.delete()
        else:
            await ctx.send("This is not a Modmail ticket channel!") # Your can Change this Message to your own message

        # Sending Transscript File and Delete
        topic = ctx.channel.topic
        if topic:
            member = ctx.guild.get_member(int(topic))
            if member:
                with open(filename, "rb") as f:
                    embed=discord.Embed(title="❌ Your ticket has been closed!", description="Your transcript is attached", color=0x245400)# Your can Change this Message and Color to your own message and Color
                    await member.send(embed=embed)
                    await member.send(file=discord.File(f, filename))

        # Delete File after sending
        os.remove(filename)

async def setup(bot):
    await bot.add_cog(ModmailSystem(bot))