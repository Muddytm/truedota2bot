import discord
from discord.ext import commands
import logging
import sys
import yaml

bot = commands.Bot(command_prefix="!mud", description="Bork bork bork")

logging.basicConfig(level=logging.INFO)


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("Prefix: " + bot.command_prefix)
    print("------")
    picture = open("icon.png", "rb")
    picture_bits = picture.read()
    picture.close()
    await bot.edit_profile(avatar=picture_bits)
    print("Updated profile")


with open("config_discord.yml") as file:
    config = yaml.safe_load(file)

token = config["token"]

bot.run(token)
