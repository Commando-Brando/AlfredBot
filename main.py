# bot.py
import os
import random
import json

from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv

data_file = "data/data.json"

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


@bot.command(name='next', help="Gets the next upcoming assignment(s).")
async def next(ctx, course_num):
    found = False

    # search through all channels and
    # match channel name with channel_id
    for channel in ctx.guild.channels:
        if channel.name == course_num:
            channel_id = str(channel.id)
            found = True

    while(found):
        # open file
        with open(data_file) as f:
            data = json.load(f)

        # sort date
        list_of_dates = []
        for date in data[channel_id]['due_dates']:
            list_of_dates.append(date)
        list_of_dates.sort(key=lambda date: datetime.strptime(date, '%m/%d/%y'))

        # check for assignments
        if channel_id in data:
            for assignment in data[channel_id]['due_dates'][list_of_dates[0]]:
                await ctx.send(f"Next assignment: {assignment} on {list_of_dates[0]}")
            return None

    # no course exist
    await ctx.send("Sorry, course does not exist.")

bot.run(TOKEN)
