#bot.py

#Gabrielle Albrecht
#Richard Gonzalez
#Corbin Styles

#RowdyHacks!!!


import os
import discord
import random
import json
import re
from re import search
from discord.ext import commands
from datetime import datetime
from dateutil import *
from datetime import datetime, time


#from dotenv import load_dotenv
#load_dotenv()
#TOKEN = os.getenv('DISCORD_TOKEN')

TOKEN = ''  # Alfred

#create data folder if DNE
if not os.path.exists('data'):
    os.makedirs('data')

# File names
courses_file = "data/courses.json"
students_file = "data/students.json"

bot = commands.Bot(command_prefix='!')

#On ready


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

#Quotes


@bot.command(name='quote', help='Random quotes')
async def Alfred_quote(ctx):

    quotes = [
        'Intrepid? I rather think of myself as "dauntless"',
        'Yes sir, we are all doomed',
        'You Start Pretending To Have Fun, You Might Even Have A Little By Accident.',
        "Don't Worry, Master Wayne. Takes A Little Time To Get Back In The Swing Of Things.",
        "They'll Hate You For It, But That's The Point Of Batman.",
        "You're Just Waiting, Hoping For Things To Go Bad Again.",
        "Things Always Get Worse Before They Get Better.",
        "Why Do We Fall, Sir? So That We Can Learn To Pick Ourselves Up."
    ]

    response = random.choice(quotes)
    await ctx.send(response)


#DM someone from a bot
@bot.command(pass_context=True, help="Alfred direct messages a specific user")
async def DM(ctx, user: discord.User, *, message):
    message = message or "This Message is sent via DM"
    await user.send(message)

#Have the bot PM you _ so you can ask about your events privately


@bot.command(name='PM', help="Alfred private messages you")
async def PrivateMessage(ctx):
    await ctx.author.send('Hello sir, you asked me to PM you.\nHow can I be of service?')


#If there is an error (missing argument)
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send("You are missing an argument. Try !help")


#~~~~Student~~~~~

#Create a student calendar
@bot.command(name='myCal', help='Create your own calendar')
async def CreateOwnCalendar(ctx):

    #If file exists check if student Id exists. If it doesn't then add channel calandar.
    #If it does then return

    student_id = str(ctx.author.id)
    try:
        #check if file exists
        if(os.path.isfile(students_file)):
            await ctx.send("File exists")

            # open file
            # with open(students_file, "r") as infile:
            #     json_object = json.load(infile)
            #     infile.close()
            #     print(json_object)
            #     print(json_object[student_id])
            #if json_object[student_id]:
            #    await ctx.send("student id exists")
            #    return

        new_data = {
            "student_name": str(ctx.author),
            "course_name": str(ctx.channel.name),
            "assignment": None
        }

        # load file
        with open(students_file) as outfile:
            json_object = json.load(outfile)
            json_object[student_id] = new_data
            outfile.close()

        # save file
        with open(students_file, 'w') as f:
            json.dump(json_object, f)
            f.close()

        await ctx.send("Event added to calendar")
    except IOError:
        await ctx.send("There is a problem")


##Add to a student calendar
@bot.command(name='addMyCal', help='add to your calendar')
async def add_cal(ctx, due_date, due_time, *, assignment):
    # alfred assigns user id
    student_id = str(ctx.author.id)

    # check if date formatted correctly
    r = re.search(r"^[01][0-9]/[0-3][0-9]/[0-9]{2}$", due_date)
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
        with open(students_file, "r") as outfile:
            json_object = json.load(outfile)

            index_length = len(
                json_object[student_id]['assignment']) + 1

            json_object[student_id]['assignment'][str(index_length)] = new_data

        # save file
        with open(students_file, 'w') as f:
            json.dump(json_object, f)
        f.close()
        await ctx.send("Event added to calendar")
    except IOError:
        await ctx.send("There was a problem")


#Get the next 10 student events
#In progress
##@bot.command(name='getMyCal', help='Get your a list of all your events')
##async def myEvents(ctx):
##    while(True):
##        # open file
##        with open(courses_file) as f:
##            data = json.load(f)
##
##        if ctx.author.id == data.student_id:
##            await ctx.send("student has a calendar")
##        else:
##            return


#MyNext
#Gives the student their next event
@bot.command(name='myNext', help='Get the next event from your own calendar')
async def myNext(ctx, section_id):
    channel_id = str(ctx.channel.id)

    try:
        while(True):
            # open file
            with open(students_file) as f:
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


###MyDelete
##@bot.command(name='myDelete', help='delete an event from your own calendar')
##async def myDelete(ctx):

##Work in progress (Ran out of time)

##Want to add modify an event


##~~~~Course~~~~~

#Create
#If file exists check if channel exists. If it doesn't then add channel calandar.
#If it does then return
@bot.command(name='create', help='Create a calendar')
async def create(ctx, section_num):

    # check if instructor
    substring = "Instructor"
    if not search(substring, str(ctx.author.roles)):
        await ctx.send("You are not an instructor")
        return

    channel_id = str(ctx.channel.id)

    #check if file exists
    if(os.path.isfile(courses_file)):
        await ctx.send("File exists")
        try:
            # open file
            with open(courses_file, "r") as outfile:
                json_object = json.load(outfile)
                outfile.close()
                print(json_object)
                if json_object[channel_id]:
                   await ctx.send("Channel exists")
                   return
        except IOError:
            await ctx.send("There is a problem")

    else:

        new_data = {
            channel_id: {
                "course_name": str(ctx.channel.name),
                "section_id": {
                    section_num
                }
            }
        }

        try:
            with open(courses_file, "a") as outfile:
                outfile.write(json.dumps(new_data))
                outfile.close()
                await ctx.send("Event added to calendar")
        except IOError:
            await ctx.send("There is a problem")


@bot.command(name='addSection', help='Add section for a channel')
async def addSection(ctx, section_num):
    # check if instructor
    substring = "Instructor"
    if not search(substring, str(ctx.author.roles)):
        await ctx.send("You are not an instructor")
        return

    channel_id = str(ctx.channel.id)

    #check if file exists
    if(os.path.isfile(courses_file)):
        try:
            # open file
            with open(courses_file, "r") as outfile:
                json_object = json.load(outfile)
                outfile.close()
                print(json_object)
                if json_object[channel_id]:
                   await ctx.send("Channel exists")

                new_data = {
                    "section_num": section_num
                }
                try:
                    # open file
                    with open(courses_file, "r") as outfile:
                        json_object = json.load(outfile)

                        if json_object[channel_id]['section_id'] != section_num:

                            index_length = len(
                                json_object[channel_id]['section_id']) + 1

                            json_object[channel_id]['section_id'][str(
                                index_length)] = new_data

                            # save file
                            with open(courses_file, 'w') as f:
                                print(json.dump(json_object, f))
                                json.dump(json_object, f)
                            outfile.close()
                            await ctx.send("Section added to calendar")
                except IOError:
                    await ctx.send("There was a problem")
        except IOError:
            await ctx.send("There was a problem")


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
    r = re.search(r"^[01][0-9]/[0-3][0-9]/[0-9]{2}$", due_date)
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
        with open(courses_file) as outfile:
            json_object = json.load(outfile)

            index_length = len(
                json_object[channel_id]['section_id'][section_num]['assignment']) + 1

            json_object[channel_id]['section_id'][section_num]['assignment'][str(
                index_length)] = new_data

        # save file
        with open(courses_file, 'w') as f:
            json.dump(json_object, f)

        await ctx.send("Event added to calendar")
    except IOError:
        await ctx.send("There was a problem")


#get next from courses calendar
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
            with open(courses_file) as f:
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

#List function
@bot.command(name='list', help="List all upcoming assignments.")
async def list(ctx, section_id):
    # alfred assigns channel id
    channel_id = str(ctx.channel.id)

    # open file
    with open(courses_file) as f:
        data = json.load(f)

    if channel_id in data:
        assignment = data[channel_id]['section_id'][section_id]['assignment']
        for key, value in assignment.items():
            await ctx.send(f"{key}: {value['name']} on {value['due_date']} at {value['time_due']}")

        return None


## Work in progress (Ran out of time) but want to do

#Delete an event from courses calendar
##@bot.command(name='delete', help='Delete event from a calendar')
##async def deleteEvent(ctx, section_id, key):
##    try:
##        # if course is found within server
##        found = False
##
##        # search through all channels and
##        # match channel name with channel_id
##        for channel in ctx.guild.channels:
##            if channel_id == str(channel.id)
##                found = True  # found course
##
##        # if channel_id found in database
##        while(found):
##            # open file
##            with open(courses_file) as f:
##                data = json.load(f)
##
##            # check for assignments
##            if channel_id in data:
##                for value in data[channel_id]['section_id'][section_id]['assignment'].values():
##                    if value['assignment'] == key:
##                        del value['assignment']
##                return None
##
##        # no course exist
##        await ctx.send("Sorry, course not found.")
##    except:
##        # section id not found
##        await ctx.send("Sorry, assignment to delete not found.")

## Want to add so that you can modify an event

## Add reminder
#~~ Partial code to get how much time is left.

##Specified date
##    date = (due_date + " " + due_time)
##    date1 = datetime.strptime(date, '%m/%d/%Y %H:%M')
##
###Current date
##    #currTime = datetime.now()
##    date2 = datetime.now()
##
##    await ctx.send("Added assignment to the calendar at: "+ str(date2) + " which is due at: " + str(date1))
##    await ctx.send("(" + "%d days, %d hours, %d minutes %d seconds" % dhms_from_seconds(date_diff_in_seconds(date1, date2))+")")
##
##def date_diff_in_seconds(dt2, dt1):
##    timedelta = dt2 - dt1
##    return timedelta.days * 24 * 3600 + timedelta.seconds
##
##def dhms_from_seconds(seconds):
##	minutes, seconds = divmod(seconds, 60)
##	hours, minutes = divmod(minutes, 60)
##	days, hours = divmod(hours, 24)
##	return (days, hours, minutes, seconds)

## Add timer


#Run program
bot.run(TOKEN)
