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

#from dotenv import load_dotenv
#load_dotenv()
#TOKEN = os.getenv('DISCORD_TOKEN')
#GUILD = os.getenv('DISCORD_GUILD')

TOKEN = 'ODI1MjAxMjI3MTM3NTQ4MzI5.YF6eiA.nZa45Ra_yeEd6dr7M84jJP-ijw0' #Alfred
#TOKEN = 'ODI1MTc0MzcxMTM1MTI3NTcz.YF6FhQ.jH_CtT-0dGjfpuFH9lix7_Eoqao'#AlfredBot

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

    quotes= [
            'Intrepid? I rather think of myself as "dauntless"',
            'Yes sir, we are all doomed',
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
        if isinstance(error,commands.errors.MissingRequiredArgument):
                await ctx.send("You are missing an argument. Try !help")


#Student events
@bot.command(name='myCal', help='Create your own calendar')
async def myEvents(ctx):

    r = re.search(r"^[01][02]/[0-3][0-9]/[0-9]{2}$", due_date)
    if not r:
       await ctx.send("Please provide the due date in this format: MM/DD/YY")
       return
    
    
    jsonFile = {
        "student_name" : str(ctx.author),
        "student_id" : str(ctx.author.id),
        "section_num": section_num,
        "assignment_info": assignment,
        "Due_Date": due_date,
        "Due_time": due_time
    }

    try:
        with open(students_file, "a") as outfile:
            json_object = json.dumps(jsonFile, indent = 4)
            outfile.write(json_object)
            outfile.close()
            await ctx.send("Event added to calendar")
    except IOError:
        await ctx.send("There was a problem")

#Get student events
@bot.command(name='getMyCal', help='Get your calendar')
async def myEvents(ctx):
    while(True):
        # open file
        with open(courses_file) as f:
            data = json.load(f)
    
        if ctx.author.id == data.student_id:
            await ctx.send("student has a calendar")
        else:
            return

    
#MyNext

#MyDelete

#Add to courses calendar
@bot.command(name='add', pass_context=True, help='Add event to a calendar')
async def add(ctx, section_num, due_date, due_time, *, assignment):

    substring = "Instructor"
    if not search(substring,str(ctx.author.roles)):
        await ctx.send("You are not an instructor")
        return
        
    r = re.search(r"^[01][02]/[0-3][0-9]/[0-9]{2}$", due_date)
    if not r:
       await ctx.send("Please provide the due date in this format: MM/DD/YY")
       return
    
    jsonFile = {
        "channel_id" : str(ctx.channel.id),
        "section_num": section_num,
        "assignment_info": assignment,
        "Due_Date": due_date,
        "Due_time": due_time
    }

    try:
        with open(courses_file, "a") as outfile:
            json_object = json.dumps(jsonFile, indent = 4)
            outfile.write(json_object)
            outfile.close()
            await ctx.send("Event added to calendar")
    except IOError:
        await ctx.send("There was a problem")   

    
    




#get next from courses calendar
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
        with open(courses_file) as f:
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


#Delete an event from courses calendar
#@bot.command(name='delete', help='Delete event from a calendar')
#async def deleteEvent(ctx, section_num, due_date, due_time, *, assignment):

   



#Get all from courses calendar
@bot.command(name='list', help='List all events for a calendar')
async def ListAll(ctx):
    
    keyVal = ctx.channel.id

    with open(courses_file, 'r') as openfile:
        json_object = json.load(openfile)
        openfile.close()
    print(json_object)
    print(json_object["channel_id"])

    x = json_object.channel_id

    #f(
##    try:
##        if keyVal in json_object:
##            print('here')
##            await ctx.send("list for channel")
##        else:
##            await ctx.send("There are no upcoming events for this channel")
##    except:
##        await ctx.send("There was a problem")   

 

#Run program
bot.run(TOKEN)
