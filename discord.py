# Derived from a modification of a test script by Rapptz, by TAOTheCrab, by me.
# (You get all that?)

import discord
import logging
import tasks

client = discord.Client()

logging.basicConfig(level=logging.INFO)


@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")


@client.event
async def on_message(message):
    # We do not want the bot to reply to itself
    if message.author == client.user:
        return

    info = (client, message)

    await tasks.general.run(*info)


with open("config_discord.yml") as file:
    config = yaml.safe_load(file)

token = config["token"]

client.run(token)
