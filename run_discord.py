# Derived from a modification of a test script by Rapptz, by TAOTheCrab, by me.
# (You get all that?)

import discord
import logging
import td2tasks
import yaml

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

    if "!patchnotes" in message.content:
        response = td2tasks.patchnotes.run(message.content)
        if response and response != "":
            name = response.split("]")[0][1:]
            response = ("**" + name + "**" + response.split("):")[1])
            await client.send_message(message.channel, response)

    if "!teamsummary" in message.content:
        response = td2tasks.newteamsummary.run(message.content)
        if response and response != "":
            await client.send_message(message.channel, response)


with open("config_discord.yml") as file:
    config = yaml.safe_load(file)

token = config["token"]

client.run(token)
