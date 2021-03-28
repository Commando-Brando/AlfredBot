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
async def next(ctx, course_num, section_id):
    try:
        # if course is found within server
        found = False

        # search through all channels and
        # match channel name with channel_id
        for channel in ctx.guild.channels:
            if channel.name == course_num:
                channel_id = str(channel.id)
                found = True  # found course

        # if channel_id found in database
        while(found):
            # open file
            with open(data_file) as f:
                data = json.load(f)

            # sort date
            list_of_dates = []
            for value in data[channel_id]['section_id'][section_id]['assignment'].values():
                list_of_dates.append(value['due_date'])
            list_of_dates.sort(
                key=lambda date: datetime.strptime(date, '%m/%d/%y'))

            # check for assignments
            if channel_id in data:
                for value in data[channel_id]['section_id'][section_id]['assignment'].values():
                    if value['due_date'] == list_of_dates[0]:
                        await ctx.send(f"Next assignment: {value['name']} on {list_of_dates[0]}")
                return None

        # no course exist
        await ctx.send("Sorry, course not found.")
    except:
        # section id not found
        await ctx.send("Sorry, section ID not found.")

bot.run(TOKEN)
