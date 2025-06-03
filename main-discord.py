import discord
from discord.ext import commands
import datetime
from datetime import timedelta
import random
import asyncio
import aiohttp
import sys
import os
from dotenv import load_dotenv

load_dotenv()
PREFIX = os.getenv("DISCORDBOTPREFIX")
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix=PREFIX, intents=intents)
client.remove_command("help")

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

@client.command()
async def help(ctx):
    embed = discord.Embed(title="HELP MENU", description="Here is my List of Commands", color=(40191))
    embed.add_field(name="CORE COMMANDS", value=f"{PREFIX}help - This message\n{PREFIX}ping - Checks my latency\n{PREFIX}giveaway - Setup a giveaway in your channel\n{PREFIX}poll - Create a 2 answer poll", inline=False)
    embed.add_field(name="OTHER COMMANDS", value=f"{PREFIX}say - Make me say stuff\n{PREFIX}esay - Make me say stuff in an embed\n{PREFIX}rps - Play Rock Paper Scissors with the bot\n{PREFIX}numberguessing - Play the Number guessing game with the bot/n{PREFIX}serverinfo - Get information about your server", inline=False)
    await ctx.send(embed=embed)

@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! My Latency is {round(client.latency * 1000)}ms")
    
@client.command()
@commands.has_permissions(manage_guild=True)
async def giveaway(ctx, time_unit: str, winners: int, *, prize: str):
    embed = discord.Embed(title="Giveaway!", description=f"{prize}", color=discord.Color.random())
    embed.add_field(name="Hosted by:", value=ctx.author.mention)
    embed.add_field(name="React with 🎉 to enter!", value=f"Ends {time_unit} from now")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("🎉")
    duration_seconds = convert(time_unit)
    await asyncio.sleep(duration_seconds)
    new_msg = await ctx.channel.fetch_message(msg.id)
    
    users = []
    async for user in new_msg.reactions[0].users():
        if user != client.user:
            users.append(user)
            
    if winners < 1:
        winners = 1 
    if len(users) <= winners:
        selected_winners = users
    else:
        selected_winners = random.sample(users, winners)

    winners_mention = ", ".join(user.mention for user in selected_winners)
    await ctx.send(f"Congratulations {winners_mention}! You won {prize}!")

@giveaway.error
async def giveaway_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You are missing permissions. You need the ``MANAGE_GUILD`` Permission to use this command')
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"This command requires some arguments: {PREFIX}giveaway <time> <winners> <prize>")
    else:
        raise error

@client.command()
@commands.has_permissions(manage_messages=True)
async def poll(ctx, question, *options: str):
    if len(options) > 2:
        await ctx.send('Something went wrong when creating the poll. If this keeps happening, Please report it to the support server')
        return
    if len(options) == 2 and options[0] == "yes" and options[1] == "no":
        reactions = ['1️⃣', '2️⃣']
    else:
        reactions = ['1️⃣', '2️⃣']
    description = []
    for x, option in enumerate(options):
        description += '\n {} {}'.format(reactions[x], option)
    poll_embed = discord.Embed(title=question, color=65400, description=''.join(description))
    react_message = await ctx.send(embed=poll_embed)
    for reaction in reactions[:len(options)]:
        await react_message.add_reaction(reaction)

@poll.error
async def poll_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You are missing permissions. You need the ``MANAGE_GUILD`` Permission to use this command')
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"This command requires some arguments: {PREFIX}poll <'question'> <'answer1'> <'answer2'>")
    else:
        raise error

@client.command()
async def serverinfo(ctx):
    format = "%a, %b %d %Y | %H:%M:%S %ZGMT"   
    nonbots = [user for user in ctx.guild.members if user.bot == False]
    embed = discord.Embed(title=f"Server Info for {ctx.guild.name}", description="Guild Name: {ctx.guild.name}\nMember Count: {ctx.guild.member_count}\nHumans Count: {len(nonbots)}\nGuild ID: {ctx.guild.id}\nServer Owner: {ctx.guild.owner}\nVerification Level: {ctx.guild.verification_level}\nServer Creation Date: {ctx.guild.created_at.strftime(format)}", color=(65400))
    text_channels = len(ctx.guild.text_channels)
    voice_channels = len(ctx.guild.voice_channels)
    categories = len(ctx.guild.categories)
    channels = text_channels + voice_channels
    embed.add_field(name="Channel Count", value=f"Categories; **{categories}**\nText Channels; **{text_channels}**\nVoice Channels; **{voice_channels}**\nTotal Channels: **{channels}**", inline=False)
    embed.set_thumbnail(url=ctx.guild.icon)
    await ctx.send(embed=embed)

@client.command()
async def say(ctx, *, question: commands.clean_content):
    await ctx.send(f'{question}')
    await ctx.message.delete()

@say.error
async def say_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("What do you want me to say?")
    else:
        raise error

@client.command()
async def esay(ctx, *, question):
    embed = discord.Embed(description=f'{question}', color=(40191))
    await ctx.send(embed=embed)
    await ctx.message.delete()

@esay.error
async def esay_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("What do you want me to say?")
    else:
        raise error

@client.command()
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

@client.command()
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
        await ctx.send(f"You didnt guess the right number within 10 tries which means you lost. You can try again by using {PREFIX}numberguessing")





TOKEN = os.getenv("DISCORDBOTTOKEN")
client.run(TOKEN)
