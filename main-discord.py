import discord
from discord.ext import commands
import datetime
from datetime import timedelta
import random
import asyncio
import aiohttp
import sys

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix=commands.when_mentioned_or('='), intents=intents)
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
    embed.add_field(name="CORE COMMANDS", value="=help - This message\n=ping - Checks my latency\n=giveaway - Setup a giveaway in your channel\n=poll - Create a 2 answer poll", inline=False)
    embed.add_field(name="OTHER COMMANDS", value="=say - Make me say stuff\n=esay - Make me say stuff in an embed", inline=False)
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
        await ctx.send("This command requires some arguments: =giveaway <time> <winners> <prize>")
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
        await ctx.send("This command requires some arguments: =poll <'question'> <'answer1'> <'answer2'>")
    else:
        raise error

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



client.run("BOTTOKENHERE")
