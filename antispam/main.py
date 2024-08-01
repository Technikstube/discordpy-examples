import discord
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

TIME_WINDOW_SECS = 5.0
MAX_MESSAGES = 5
DELETE_MESSAGES = MAX_MESSAGES

# Keep in mind to activate the intents in the dev portal.
intents = discord.Intents.all()

bot = discord.Client(intents=intents)

# Store message counts in specific time periods for each user
messages = {}

@bot.event
async def on_ready():
    print("Antispam successfully started!")
    print(f"User: {bot.user} ({bot.user.id})")

@bot.event
async def on_message(message: discord.Message):

    # Ignore all bots
    if message.author.bot:
        return

    guild_id = message.author.guild.id
    member_id = message.author.id
    message_id = message.id

    if not messages.get(guild_id):
        messages[guild_id] = {}

    antispam_guild = messages[guild_id]

    if not antispam_guild.get(member_id):
        antispam_guild[member_id] = {
            "last_message": datetime.now(), 
            "count": 0
        }

    antispam_guild_member = antispam_guild[member_id]

    last_message = antispam_guild_member["last_message"]

    if (datetime.now() - last_message).seconds >= TIME_WINDOW_SECS:
        del messages[guild_id][member_id]
        return

    antispam_guild_member["count"] += 1

    if antispam_guild_member["count"] == MAX_MESSAGES:
        del messages[guild_id][member_id]

        await message.channel.send(f"> {message.author.mention} please don't spam!", delete_after=5.0)

        # Delete last messages from user
        await message.channel.purge(limit=DELETE_MESSAGES, check=lambda m: m.author.id == member_id)

        



bot.run(os.environ.get("BOT_TOKEN"))