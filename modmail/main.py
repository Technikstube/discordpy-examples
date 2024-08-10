from dotenv import load_dotenv
import discord
from discord.ext import commands
import os

load_dotenv()
bot = commands.Bot(command_prefix="-", intents=discord.Intents.all())
 
@bot.event
async def on_ready():
    print("Bot gestartet!") # You can Change the Message

    await load()
    
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(os.getenv("TOKEN"))
