import voltage
from voltage.ext import commands
import datetime
from datetime import timedelta
import random
import asyncio
import aiohttp
import json
import os
from dotenv import load_dotenv

load_dotenv()
PREFIX = os.getenv("REVOLTBOTPREFIX")
client = commands.CommandsClient(PREFIX)

def convert(time):
  pos = ["s","m","h","d"]

  time_dict = {"s" : 1, "m" : 60, "h" : 3600, "d": 3600*24}

  unit = time[-1]

  if unit not in pos:
    return -1
  try:
    val = int(time[:-1])
  except:
    return -2

  return val * time_dict[unit]

@commands.is_server_owner()
@client.command(description="Setup a giveaway in your channel")
async def giveaway(ctx, time_unit: str, winners: int, *, prize: str):
    embed = voltage.SendableEmbed(title="Giveaway!", description=f"Prize: {prize}\nReact with 🎉 to enter!\nEnds {time_unit} from now", color="#DE00A0")
    msg = await ctx.send(embed=embed)
    await msg.react("🎉")
    duration_seconds = convert(time_unit)
    await asyncio.sleep(duration_seconds)
    new_msg = await ctx.channel.fetch_message(msg.id)
    
    members = []

    winners_mention = random.choice(new_msg.reactions["🎉"])
    await ctx.send(f"Congratulations {winners_mention}! You won {prize}!")

@commands.is_server_owner()
@client.command(description="Create a 2 answer poll")
async def poll(ctx, question, option1: str, option2: str):
    poll_embed = voltage.SendableEmbed(title=question, color="#DE00A0", description=f"1️⃣ {option1}\n2️⃣ {option2}")
    new_msg = await ctx.send(embed=poll_embed)
    await new_msg.react('1️⃣')
    await new_msg.react('2️⃣')

@client.command(description="Get information about your server")
async def serverinfo(ctx):
    embed = voltage.SendableEmbed(title=f"Server Information for {ctx.server.name}", description=f"Guild Name: {ctx.server.name}\nGuild ID: {ctx.server.id}\nServer Owner: {ctx.server.owner.name} (`{ctx.server.owner.id}`)\nServer Creation Date: {ctx.server.created_at}", media=ctx.server.icon, color="#00FF4F")
    await ctx.send(embed=embed)

@client.command(description="Make the bot say your message")
async def say(ctx, *, question):
    await ctx.send(f'{question}')
    await ctx.message.delete()

@client.command(description="Make the bot say your message in an embed")
async def esay(ctx, *, question):
    embed = voltage.SendableEmbed(description=f'{question}', color='#00FF4F')
    await ctx.send(embed=embed)
    await ctx.message.delete()

@client.command(description="Play Rock Paper Scissors with the bot")
async def rps(ctx):
    rpsGame = ['rock', 'paper', 'scissors']
    await ctx.send(f"Time to play Rock Paper Scissors. Choose: rock, paper, scissors")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in rpsGame

    user_choice = (await client.wait_for('message', check=check)).content

    comp_choice = random.choice(rpsGame)
    if user_choice == 'rock':
        if comp_choice == 'rock':
            await ctx.send(f"Your Status: Tied\nYour choice: {user_choice}\nMy choice: {comp_choice}")
        elif comp_choice == 'paper':
            await ctx.send(f"Your Status: Lost\nYour choice: {user_choice}\nMy choice: {comp_choice}")
        elif comp_choice == 'scissors':
            await ctx.send(f"Your Status: Won\nYour choice: {user_choice}\nMy choice: {comp_choice}")

    elif user_choice == 'paper':
        if comp_choice == 'rock':
            await ctx.send(f"Your Status: Won\nYour choice: {user_choice}\nMy choice: {comp_choice}")
        elif comp_choice == 'paper':
            await ctx.send(f"Your Status: Tied\nYour choice: {user_choice}\nMy choice: {comp_choice}")
        elif comp_choice == 'scissors':
            await ctx.send(f"Your Status: Lost\nYour choice: {user_choice}\nMy choice: {comp_choice}")

    elif user_choice == 'scissors':
        if comp_choice == 'rock':
            await ctx.send(f"Your Status: Lost\nYour choice: {user_choice}\nMy choice: {comp_choice}")
        elif comp_choice == 'paper':
            await ctx.send(f"Your Status: Won\nYour choice: {user_choice}\nMy choice: {comp_choice}")
        elif comp_choice == 'scissors':
            await ctx.send(f"Your Status: Tied\nYour choice: {user_choice}\nMy choice: {comp_choice}")

@client.command(description="Play the Number Guessing game with the bot")
async def numberguessing(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.message.channel
    number = random.randint(1, 100)
    await ctx.send("Time to play the number guessing game. I am thinking of a number between 1 and 100. You get 10 chances.")

    for i in range(0, 10):
        guess = await client.wait_for('message', check=check)
        if guess.content == str(number):
            await ctx.send("You guess the right number which means you won. You can run =numberguessing if you want to play again")
            return
        elif guess.content < str(number):
            await ctx.send('Higher!')
        elif guess.content > str(number):
            await ctx.send('Lower!')
        else:
            return     
    else:
        await ctx.send("You didnt guess the right number within 10 tries which means you lost. You can try again by using =numberguessing")





TOKEN = os.getenv("REVOLTBOTTOKEN")
client.run(TOKEN)
