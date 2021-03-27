# bot.py
import os
import random
import json

from discord.ext import commands
from dotenv import load_dotenv

data_file = "data/test.json"

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


@bot.command(name='test', help="Debug: testing courses.")
async def name(ctx):
    user_name = ctx.message.author.name
    with open(data_file) as f:
        data = json.load(f)
    if user_name in data:
        for val in data[user_name].values():
            await ctx.send(f"{val['name']}, Section {val['section']} on {val['days']}")
    else:
        await ctx.send("Sorry, I could not find you in the database.")


bot.run(TOKEN)
