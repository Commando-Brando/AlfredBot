import os
import random
import json
import re

from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv
from re import search

data_file = "data/data.json"

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


@bot.command(name='add', pass_context=True, help='Add event to a calendar')
async def add(ctx, section_num, due_date, due_time, *, assignment):
    # alfred assigns channel id
    channel_id = str(ctx.channel.id)

    # check if instructor
    substring = "Instructor"
    if not search(substring, str(ctx.author.roles)):
        await ctx.send("You are not an instructor")
        return

    # check if date formatted correctly
    r = re.search(r"^[01][02]/[0-3][0-9]/[0-9]{2}$", due_date)
    if not r:
        await ctx.send("Please provide the due date in this format: MM/DD/YY")
        return

    new_data = {
        "name": assignment,
        "due_date": due_date,
        "time_due": due_time
    }

    try:
        # open file
        with open(data_file) as outfile:
            json_object = json.load(outfile)

            index_length = len(
                json_object[channel_id]['section_id'][section_num]['assignment']) + 1

            json_object[channel_id]['section_id'][section_num]['assignment'][str(
                index_length)] = new_data
        
        # save file
        with open(data_file, 'w') as f:
            json.dump(json_object, f)

        await ctx.send("Event added to calendar")
    except IOError:
        await ctx.send("There was a problem")


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
