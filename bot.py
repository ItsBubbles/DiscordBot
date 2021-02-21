import os
import discord
import time
import random
import json
from discord.ext import commands
from discord.ext.commands import bot, BucketType, CommandOnCooldown, errors
import scrape
import tkn
from scrape import discordjoke
from scrape import discordjokesingle

client = commands.Bot(command_prefix = "!")
bot = commands.Bot(command_prefix='?')

@client.event
async def on_ready():
    print("Working")

@client.event
async def on_message(message):

    if message.content.startswith(str("<:travvypatty:769418655829196810>")):
        await message.channel.send("https://cdn.discordapp.com/attachments/321896054452649985/769591917042204713/small_trav.PNG")
  
    await client.process_commands(message)


@client.command()
async def joke(ctx):
    await ctx.send(str(scrape.discordjokesingle()))

@client.command()
async def coinflip(ctx):
    working = True
    
    await ctx.send("Heads or Tails")

    def is_correct(m):
        return m.author == ctx.author 
    
    randomcoin = random.randint(0,1)
    
    coinflipresponse = await client.wait_for("message", check = is_correct)

    await ctx.send("What is your wager")
    coinflipwager = await client.wait_for("message", check = is_correct)
    
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    bankamount = users[str(user.id)]["bank"]

    coinflipstring= str(coinflipwager.content)
    coinflipfloat = float(coinflipstring)
    coinflipmath = coinflipfloat * 0.5
    coinflipwinnings = int(coinflipmath)

    while (working == True):
        if(coinflipfloat > bankamount):
            await ctx.send("You are to broke, try again")
            working = False
            break
            
        if str(coinflipresponse.content) == "Heads":
            if randomcoin == 0:
                users[str(user.id)]["bank"] += coinflipwinnings
                with open("mainbank.json", "w") as f:
                    json.dump(users, f)

                finalem = discord.Embed(title = "CoinFlip Results", color = discord.Color.purple())
                finalem.add_field(name = "Heads", value = f"You won {coinflipwinnings} $")
                await ctx.send (embed = finalem)
                working = False

            else:
                coinfliplosings = coinflipfloat * -1
                users[str(user.id)]["bank"] += coinfliplosings
                with open("mainbank.json", "w") as f:
                    json.dump(users, f)

                finalem = discord.Embed(title = "CoinFlip Results", color = discord.Color.purple())
                finalem.add_field(name = "Tails", value = f"You lost {coinflipfloat} $")
                await ctx.send (embed = finalem)
                working = False
        
        elif str(coinflipresponse.content) == "Tails":
            if randomcoin == 1:

                users[str(user.id)]["bank"] += coinflipwinnings
                with open("mainbank.json", "w") as f:
                    json.dump(users, f)
                
                finalem = discord.Embed(title = "CoinFlip Results", color = discord.Color.purple())
                finalem.add_field(name = "Tails", value = f"You won {coinflipwinnings} $")
                await ctx.send (embed = finalem)
                working = False
            else:
                coinfliplosings = coinflipfloat * -1
                users[str(user.id)]["bank"] += coinfliplosings
                with open("mainbank.json", "w") as f:
                    json.dump(users, f)
                    
                finalem = discord.Embed(title = "CoinFlip Results", color = discord.Color.purple())
                finalem.add_field(name = "Heads", value = f"You lost {coinflipfloat} $")
                await ctx.send (embed = finalem)
                working = False
            
@client.command()
async def balance(ctx):
    await open_account(ctx.author)

    balance = "Balance"
    user = ctx.author
    users = await get_bank_data()

    bankamount = users[str(user.id)]["bank"]

    bankem = discord.Embed(title = f"{ctx.author.name}'s Balance", color = discord.Color.purple())
    bankem.add_field(name = "Bank Amount", value = bankamount)

    await ctx.send (embed = bankem)

async def open_account(user):
    users = await get_bank_data()
    
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["bank"] = 100
        
    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    return True
    
async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f)
    return users

async def depositbankmoney():
    users = await get_bank_data()
    with open("mainbank.json", "w") as f:
        json.dump(users, f)

@client.command()
@commands.cooldown(1, 60, BucketType.default)
async def getmoney(ctx):

    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    askmoney = random.randint(0,101)

    await ctx.send("The homie hooked it up with " + str(askmoney) + " dolla bills")

    users[str(user.id)]["bank"] += askmoney

    with open("mainbank.json", "w") as f:
        json.dump(users, f)

@client.event
async def on_command_error(ctx, error):
    randomnum = str(random.randint(1,12))
    greedlist = ["Slow down big fella dont get too greedy", "Alright greedy gary", "You really are that broke man, thats tough", "Dang you really are asking for handouts", 
        f"Woah there we got got a greedy person at {randomnum} o'clock"]
        
    if isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
        await ctx.send(f'{random.choice(greedlist)}, wait %.0f seconds' % error.retry_after)

client.run(tkn.tkn)