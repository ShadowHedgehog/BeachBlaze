import voltage
from voltage.ext import commands
import datetime
from datetime import timedelta
import random
import asyncio
import aiohttp
import json

client = commands.CommandsClient("=")

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
@client.command(description="Create a 2 answer poll")
async def poll(ctx, question, option1: str, option2: str):
    poll_embed = voltage.SendableEmbed(title=question, color="#DE00A0", description=f"1️⃣ {option1}\n2️⃣ {option2}")
    new_msg = await ctx.send(embed=poll_embed)
    await new_msg.react('1️⃣')
    await new_msg.react('2️⃣')

@client.command(description="Make the bot say your message")
async def say(ctx, *, question):
    await ctx.send(f'{question}')
    await ctx.message.delete()

@client.command(description="Make the bot say your message in an embed")
async def esay(ctx, *, question):
    embed = voltage.SendableEmbed(description=f'{question}', color='#00FF4F')
    await ctx.send(embed=embed)
    await ctx.message.delete()



client.run("BOTTOKENHERE")
