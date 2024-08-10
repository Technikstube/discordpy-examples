import discord
import os
from dotenv import get_key
from discord.ext.commands import Bot
from utility import Config

TOKEN = get_key(".env", "TOKEN")

# If needed, change this to discord.Intents.all() to enable all intents. The ping slash command works with default.
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    config = Config()
    
    conf = config.get()
    
    for _guild in bot.guilds:
        if str(_guild.id) not in conf:
            
            conf[str(_guild.id)] = {}
            conf[str(_guild.id)]["owner_id"] = str(_guild.owner.id)
            conf[str(_guild.id)]["assigned_roles"] = {}
            conf[str(_guild.id)]["assigned_roles"][str(_guild.owner.id)] = 3
    
    config.save(conf)
            
    # go through the cogs folder
    for file in os.listdir("./external-permission-system/cogs/"):
        
        # check if the file ends with ".py"
        if file.endswith(".py"):
            
            # if it ends with ".py", load it
            # FYI: "[:-3]" cuts off the ".py" (3 letters/symbols) at the end of the file name
            await bot.load_extension(f"cogs.{file[:-3]}")
            print(f"Loaded Extension: {file[:-3]}")
    
    # Syncronize the slash commands to discord
    await bot.tree.sync()
    
    print("Ready!")
    

# Run the bot with the set TOKEN
bot.run(TOKEN)