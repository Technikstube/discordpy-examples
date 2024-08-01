from PIL import Image, ImageOps, ImageFont, ImageDraw, ImageFilter
import requests
from io import BytesIO
import os
import discord

IMAGE_SRC = "./images"
FONT_SRC = "./fonts"

BACKGROUND_IMAGE = f"{IMAGE_SRC}/welcome_background.png"
SERVER_NAME = "Technikstube"

# Image width and height
IMG_W, IMG_H = 960, 320

# Fixed offset to align the texts next to the avatar
TEXT_OFFSET_X = 300

# Fonts for the images, currently the same font in two different sizes
FONT_LARGE = ImageFont.truetype(font=f"{FONT_SRC}/OpenSans-Bold.ttf", size=40)
FONT_SMALL = ImageFont.truetype(font=f"{FONT_SRC}/OpenSans-Bold.ttf", size=28)

# Gets the avatar image from the user
def image_from_url(url: str):
    response = requests.get(url)
    return BytesIO(response.content)

# Processes the avatar from the user, downloads and resizes it
async def process_avatar(avatar_url, frame=1):
    response = image_from_url(avatar_url)
    avatar = Image.open(response).convert("RGBA")

    # Resize it, so it fits better in the image
    avatar = avatar.resize((210, 210))
    return avatar

# Use a mask to crop the avatar into a specific shape and paste it (See welcome_mask.jpg)
async def add_avatar(img, avatar, mask, xy=(60, 55), frame=0):
    output = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)

    img.paste(output, xy, mask=output)
    return img

async def add_background():
    img = Image.new("RGBA", (IMG_W, IMG_H))
    background = Image.open(BACKGROUND_IMAGE)

    draw = ImageDraw.Draw(img)

    # Paste it aligned to the center of the image
    img.paste(background, (int((img.width - background.width) / 2), int((img.height - background.height) / 2)))

    return img, draw

# Add the texts to the welcome image
async def add_text(draw, greeting, welcome_text):
    # Adds the greeting message with the username
    draw.text((TEXT_OFFSET_X, 130), greeting, font=FONT_LARGE)

    # Adds the welcome text with the member count
    draw.text((TEXT_OFFSET_X, 185), welcome_text, font=FONT_SMALL)

    # Adds the servername at the top
    draw.text((TEXT_OFFSET_X, 90), SERVER_NAME, font=FONT_SMALL, fill=(102, 126, 250))

# Calls all the functions needed to generate the welcome image.
# Saves the generated image and returns it as discord.File
async def generate(member: discord.Member):
    member_count = member.guild.member_count
    username = member.global_name

    welcome_text = f"We now have {member_count} members!"
    greeting = f"Welcome {username}!"

    # Display if the username is longer than the image can display
    if len(username) > 14:
        greeting = f"Welcome {username[0:14]}...!"
    
    # Gets the image mask used to crop the avatar
    mask = Image.open(f"{IMAGE_SRC}/welcome_mask.jpg").convert('L')

    img, draw = await add_background()

    avatar = await process_avatar(member.avatar.url if member.avatar is not None else member.default_avatar.url)

    await add_avatar(img, avatar, mask)

    await add_text(draw, greeting, welcome_text)

    save_path = f"{IMAGE_SRC}/welcome.png"

    img.save(save_path)

    return discord.File(save_path)