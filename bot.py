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
dealercardrandom = 0


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
@commands.cooldown(1,5)
async def blackjack(ctx):
    global dealercardrandom
    usercard1 = random.randint(1,11)
    usercard2 = random.randint(1,11)
    usercard3 = random.randint(1,11)
    usercard4 = random.randint(1,11)
    usercard5 = random.randint(1,11)
    usercard6 = random.randint(1,11)
    dealercardrandom = random.randint(1,11)
    Working = True

    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    bankamount = users[str(user.id)]["bank"]

    await ctx.send("What is your wager")
    
    def is_correct(m):
        return m.author == ctx.author 
    
    userwager = await client.wait_for("message", check = is_correct)

    userwagerread = str(userwager.content)
    userwagerint = int(userwagerread)
    userwagerwinnings = userwagerint
    userwagerlosings = userwagerint * -1
    
    while (Working == True):
        if(userwagerint> bankamount):
            await ctx.send("You are to broke, try again")
            Working = False
            break

        startem = discord.Embed(title = f"{ctx.author.name}'s Cards", color = discord.Color.purple())
        startem.add_field(name = f"Your Cards ", value = f"{usercard1}  {usercard2}")
        startem.add_field(name = f"Dealer Cards", value = f"{dealercardrandom}", inline = False)
        await ctx.send (embed = startem)

        userhit = await client.wait_for("message", check = is_correct)

        if str(userhit.content) == "Hit":
            playercardtotal = usercard1 + usercard2 + usercard3
        
            if (playercardtotal > 21):
                bustem = discord.Embed(title = f"{ctx.author.name}'s Losings ", color = discord.Color.purple())
                bustem.add_field(name = f"BUST", value = f"{playercardtotal}")
                bustem.add_field(name = f"You lost", value = f"{str(userwager.content)} $")
                await ctx.send(embed = bustem)
                users[str(user.id)]["bank"] += userwagerlosings
                with open("mainbank.json", "w") as f:
                    json.dump(users, f)
                Working == False

            else:
                hitem = discord.Embed(title = f"{ctx.author.name}'s Cards", color = discord.Color.purple())
                hitem.add_field(name = f"Your Cards ", value = f"{usercard1}  {usercard2}  {usercard3}")
                hitem.add_field(name = f"Dealer Cards", value = f"{dealercardrandom}", inline = False)
                await ctx.send (embed = hitem)
                working = True

        if str(userhit.content) == "Stand":

            dealercardtotal1 = getnumber17(dealercardrandom)
            print(dealercardtotal1)

            playercardtotal = usercard1 + usercard2
            
            if (dealercardtotal1 <= 21 and dealercardtotal1 >= 17 and dealercardtotal1 < playercardtotal):
                standem = discord.Embed(title = f"{ctx.author.name}'s Winnings", color = discord.Color.purple())
                standem.add_field(name = f"Dealers Cards", value = f"{dealercardtotal1}")
                standem.add_field(name = f"Your Cards", value = f"{playercardtotal}")
                standem.add_field(name = f"Winnings", value = f"{userwagerwinnings} $")
                users[str(user.id)]["bank"] += userwagerwinnings
                with open("mainbank.json", "w") as f:
                    json.dump(users, f)
                await ctx.send(embed = standem)
                Working = False
                
            
            elif (dealercardtotal1 > 21):
                
                standem1 = discord.Embed(title = f"{ctx.author.name}'s Winnings", color = discord.Color.purple())
                standem1.add_field(name = f"Dealers Cards", value = f"{dealercardtotal1}")
                standem1.add_field(name = f"Your Cards", value = f"{playercardtotal}")
                standem1.add_field(name = f"Winnings", value = f"{userwagerwinnings} $")
                users[str(user.id)]["bank"] += userwagerwinnings
                with open("mainbank.json", "w") as f:
                    json.dump(users, f)
                await ctx.send (embed = standem1)
                Working = False

            elif (dealercardtotal1 > playercardtotal):
                standem2= discord.Embed(title = f"{ctx.author.name}'s You lost", color = discord.Color.purple())
                standem2.add_field(name = f"Your Cards ", value = f"{playercardtotal}")
                standem2.add_field(name = f"Dealer Cards", value = f"{dealercardtotal1}")
                standem2.add_field(name = f"Losings", value = f"{userwager.content} $")
                users[str(user.id)]["bank"] += userwagerlosings
                with open("mainbank.json", "w") as f:
                    json.dump(users, f)
                await ctx.send (embed = standem2)
                Working = False

            
        userhit2 = await client.wait_for("message", check = is_correct)

        if str(userhit2.content) == "Hit":

            playercardtotal = usercard1 + usercard2 + usercard3 + usercard4

            if (playercardtotal > 21):
                bustem2 = discord.Embed(title = f"{ctx.author.name}'s Losings", color = discord.Color.purple())
                bustem2.add_field(name = f"BUST", value = f"{playercardtotal}")
                bustem2.add_field(name = f"You lost", value = f"{str(userwager.content)} $")
                users[str(user.id)]["bank"] += userwagerlosings
                with open("mainbank.json", "w") as f:
                    json.dump(users, f)
                await ctx.send(embed = bustem2)
                working = False

            else:
                hitem2 = discord.Embed(title = f"{ctx.author.name}'s Cards", color = discord.Color.purple())
                hitem2.add_field(name = f"Your Cards ", value = f"{usercard1}  {usercard2}  {usercard3}  {usercard4}")
                hitem2.add_field(name = f"Dealer Cards", value = f"{dealercardrandom}", inline = False)
                await ctx.send (embed = hitem2)
                Working = True
        if str(userhit2.content) == "Stand":
            dealercardtotal1 = getnumber17(dealercardrandom)
            print(dealercardtotal1)

            playercardtotal = usercard1 + usercard2 + usercard3
            
            if (dealercardtotal1 <= 21 and dealercardtotal1 >= 17 and dealercardtotal1 < playercardtotal):
                standem = discord.Embed(title = f"{ctx.author.name}'s Winnings", color = discord.Color.purple())
                standem.add_field(name = f"Dealers Cards", value = f"{dealercardtotal1}")
                standem.add_field(name = f"Your Cards", value = f"{playercardtotal}")
                standem.add_field(name = f"Winnings", value = f"{userwagerwinnings} $")
                users[str(user.id)]["bank"] += userwagerwinnings
                with open("mainbank.json", "w") as f:
                    json.dump(users, f)
                await ctx.send(embed = standem)
                Working = False
            
            elif (dealercardtotal1 > 21):
                
                standem1 = discord.Embed(title = f"{ctx.author.name}'s Winnings", color = discord.Color.purple())
                standem1.add_field(name = f"Dealers Cards", value = f"{dealercardtotal1}")
                standem1.add_field(name = f"Your Cards", value = f"{playercardtotal}")
                standem1.add_field(name = f"Winnings", value = f"{userwagerwinnings} $")
                users[str(user.id)]["bank"] += userwagerwinnings
                with open("mainbank.json", "w") as f:
                    json.dump(users, f)
                await ctx.send (embed = standem1)
                Working = False

            elif (dealercardtotal1 > playercardtotal):
                standem2= discord.Embed(title = f"{ctx.author.name}'s You lost", color = discord.Color.purple())
                standem2.add_field(name = f"Your Cards ", value = f"{playercardtotal}")
                standem2.add_field(name = f"Dealer Cards", value = f"{dealercardtotal1}")
                standem2.add_field(name = f"Losings", value = f"{userwager.content} $")
                users[str(user.id)]["bank"] += userwagerlosings
                with open("mainbank.json", "w") as f:
                    json.dump(users, f)
                await ctx.send (embed = standem2)
                Working = False
            
            
        
        userhit3 = await client.wait_for("message", check = is_correct)

        if str(userhit3.content) == "Hit":

            playercardtotal = usercard1 + usercard2 + usercard3 + usercard4 + usercard5
        
            if (usercard1 + usercard2 + usercard3 + usercard4 + usercard5 > 21):
                bustem3 = discord.Embed(title = f"{ctx.author.name}'s Losings", color = discord.Color.purple())
                bustem3.add_field(name = f"BUST", value = f"{playercardtotal}")
                bustem3.add_field(name = f"You lost", value = f"{str(userwager.content)} $")
                users[str(user.id)]["bank"] += userwagerlosings
                with open("mainbank.json", "w") as f:
                    json.dump(users, f)
                await ctx.send(embed = bustem3)
                Working = False
            else:
                hitem3 = discord.Embed(title = f"{ctx.author.name}'s Cards", color = discord.Color.purple())
                hitem3.add_field(name = f"Your Cards ", value = f"{usercard1}  {usercard2}  {usercard3}  {usercard4} {usercard5}")
                hitem3.add_field(name = f"Dealer Cards", value = f"{dealercardrandom}", inline = False)
                await ctx.send (embed = hitem3)
                Working = True
        
            if str(userhit3.content) == "Stand":
                dealercardtotal1 = getnumber17(dealercardrandom)
                print(dealercardtotal1)

                playercardtotal = usercard1 + usercard2 + usercard3 + usercard4
                
                if (dealercardtotal1 <= 21 and dealercardtotal1 >= 17 and dealercardtotal1 < playercardtotal):
                    standem = discord.Embed(title = f"{ctx.author.name}'s Winnings", color = discord.Color.purple())
                    standem.add_field(name = f"Dealers Cards", value = f"{dealercardtotal1}")
                    standem.add_field(name = f"Your Cards", value = f"{playercardtotal}")
                    standem.add_field(name = f"Winnings", value = f"{userwagerwinnings} $")
                    users[str(user.id)]["bank"] += userwagerwinnings
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                    await ctx.send(embed = standem)
                    Working = False
                
                elif (dealercardtotal1 > 21):
                    
                    standem1 = discord.Embed(title = f"{ctx.author.name}'s Winnings", color = discord.Color.purple())
                    standem1.add_field(name = f"Dealers Cards", value = f"{dealercardtotal1}")
                    standem1.add_field(name = f"Your Cards", value = f"{playercardtotal}")
                    standem1.add_field(name = f"Winnings", value = f"{userwagerwinnings} $")
                    users[str(user.id)]["bank"] += userwagerwinnings
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                    await ctx.send (embed = standem1)
                    Working = False

                elif (dealercardtotal1 > playercardtotal):
                    standem2= discord.Embed(title = f"{ctx.author.name}'s You lost", color = discord.Color.purple())
                    standem2.add_field(name = f"Your Cards ", value = f"{playercardtotal}")
                    standem2.add_field(name = f"Dealer Cards", value = f"{dealercardtotal1}")
                    standem2.add_field(name = f"Losings", value = f"{userwager.content} $")
                    users[str(user.id)]["bank"] += userwagerlosings
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                    await ctx.send (embed = standem2)
                    Working = False
        

            userhit4 = await client.wait_for("message", check = is_correct)
            if str(userhit4.content) == "Hit":
                playercardtotal = usercard1 + usercard2 + usercard3 + usercard4 + usercard5 + usercard6

                if (usercard1 + usercard2 + usercard3 + usercard4 + usercard5  + usercard6> 21):
                    bustem4 = discord.Embed(title = f"{ctx.author.name}'s Losings", color = discord.Color.purple())
                    bustem4.add_field(name = f"BUST", value = f"{playercardtotal}")
                    bustem4.add_field(name = f"You lost", value = f"{str(userwager.content)} $")
                    users[str(user.id)]["bank"] += userwagerlosings
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                    await ctx.send(embed = bustem4)
                    Working = False
                else:
                    hitem4 = discord.Embed(title = f"{ctx.author.name}'s Cards", color = discord.Color.purple())
                    hitem4.add_field(name = f"Your Cards ", value = f"{usercard1}  {usercard2}  {usercard3}  {usercard4} {usercard5}  {usercard6}")
                    hitem4.add_field(name = f"Dealer Cards", value = f"{dealercardrandom}", inline = False)
                    await ctx.send (embed = hitem4)
                    Working = True

            
            if str(userhit4.content) == "Stand":
                dealercardtotal1 = getnumber17(dealercardrandom)
                print(dealercardtotal1)

                playercardtotal = usercard1 + usercard2 +usercard3 + usercard4 + usercard5
                
                if (dealercardtotal1 <= 21 and dealercardtotal1 >= 17 and dealercardtotal1 < playercardtotal):
                    standem = discord.Embed(title = f"{ctx.author.name}'s Winnings", color = discord.Color.purple())
                    standem.add_field(name = f"Dealers Cards", value = f"{dealercardtotal1}")
                    standem.add_field(name = f"Your Cards", value = f"{playercardtotal}")
                    standem.add_field(name = f"Winnings", value = f"{userwagerwinnings} $")
                    users[str(user.id)]["bank"] += userwagerwinnings
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                    await ctx.send(embed = standem)
                    Working = False
                
                elif (dealercardtotal1 > 21):
                    
                    standem1 = discord.Embed(title = f"{ctx.author.name}'s Winnings", color = discord.Color.purple())
                    standem1.add_field(name = f"Dealers Cards", value = f"{dealercardtotal1}")
                    standem1.add_field(name = f"Your Cards", value = f"{playercardtotal}")
                    standem1.add_field(name = f"Winnings", value = f"{userwagerwinnings} $")
                    users[str(user.id)]["bank"] += userwagerwinnings
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                    await ctx.send (embed = standem1)
                    Working = False

                elif (dealercardtotal1 > playercardtotal):
                    standem2= discord.Embed(title = f"{ctx.author.name}'s You lost", color = discord.Color.purple())
                    standem2.add_field(name = f"Your Cards ", value = f"{playercardtotal}")
                    standem2.add_field(name = f"Dealer Cards", value = f"{dealercardtotal1}")
                    standem2.add_field(name = f"Losings", value = f"{userwager.content} $")
                    users[str(user.id)]["bank"] += userwagerlosings
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                    await ctx.send (embed = standem2)
                    Working = False


def getnumber17(dealercardrandom):
    
    dealercardrandom += random.randint(1,11)
    
    while(dealercardrandom < 17):
        
        return getnumber17(dealercardrandom)
    
    return dealercardrandom


@client.command()
async def balance(ctx):
    await open_account(ctx.author)

    balance = "Balance"
    user = ctx.author
    users = await get_bank_data()

    bankamount = users[str(user.id)]["bank"]

    bankem = discord.Embed(title = f"{ctx.author.name}'s Balance", color = discord.Color.purple())
    bankem.add_field(name = "Bank Amount", value = bankamount)

    await ctx.send(embed = bankem)

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