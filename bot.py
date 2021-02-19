import os
import discord
import time
import random
from discord.ext import commands
from discord.ext.commands import bot
import scrape
import tkn
from scrape import discordjoke



client = commands.Bot(command_prefix = ".")
bot = commands.Bot(command_prefix='?')

@client.event
async def on_ready():
    print("Working")


@client.event
async def on_message(message):
    if message.content.startswith("!joke"):
        j = scrape.discordjoke()
        if j != None:
            await message.channel.send(str(scrape.discordjoke()))
        else:
            print("Broken Bot try again 5 sec")
             
    
    if message.content.startswith("broken"):
        await message.channel.send("No you're broken")

    
    if message.content.startswith(str("<:travvypatty:769418655829196810>")):
        await message.channel.send("https://cdn.discordapp.com/attachments/321896054452649985/769591917042204713/small_trav.PNG")

client.run(tkn.tkn)