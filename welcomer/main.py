import discord
from dotenv import load_dotenv
import os
import image

load_dotenv()

# Change this to your channel. In production you might want to use a configuration file or database.
WELCOME_CHANNEL = 1143997223689011294

# Keep in mind to activate the intents in the dev portal.
intents = discord.Intents.all()

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print("Welcomer successfully started!")
    print(f"User: {bot.user} ({bot.user.id})")

# This event will be fired if a member joins the server.
@bot.event
async def on_member_join(member: discord.Member):

    # Ignore all bots that are joining
    if member.bot:
        return

    # Call the function that creates the welcome image
    welcome_image = await image.generate(member)

    # Send the file to the channel
    channel = bot.get_channel(WELCOME_CHANNEL)

    await channel.send(
        f"**Welcome {member.mention}!**",
        file=welcome_image
    )

bot.run(os.environ.get("BOT_TOKEN"))