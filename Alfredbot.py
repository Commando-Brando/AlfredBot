#bot.py
import os

import discord
import random
import json
from discord.ext import commands

#from dotenv import load_dotenv
#load_dotenv()
#TOKEN = os.getenv('DISCORD_TOKEN')
#GUILD = os.getenv('DISCORD_GUILD')

#GUILD = 'Alfred Bot'

#~channel ids
cs1083ID = 825424192349667378
cs1714ID = 825424262184566804
cs3424ID = 825424217394511902
cs3443ID = 825424239883845702

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='quote')
async def Alfred_quote(ctx): 

    quotes= [
            'Intrepid? I rather think of myself as "dauntless"',
            'Yes sir, we are all doomed',
    ]

    response = random.choice(quotes)
    await ctx.send(response)
    

@bot.command(pass_context=True, help="Alfred direct messages a specific user")
async def DM(ctx, user: discord.User, *, message):
    message = message or "This Message is sent via DM"
    await user.send(message)
     
@bot.command(name='PM', help="Alfred private messages you")
async def PrivateMessage(ctx):
            await ctx.author.send('Hello sir, you asked me to PM you.\nHow can I be of service?')
    
@bot.event
async def on_command_error(ctx, error):
        if isinstance(error,commands.errors.MissingRequiredArgument):
                await ctx.send("You are missing an argument. Try !help")

@bot.command(name='add', pass_context=True, help='Add event to a calendar')
async def add(ctx, section_num, due_date, due_time, *, assignment):

    if(not re.search(r"^[01][[0-9]/[0-3][0-9]/[0-9]{2}$", due_date)):
       await ctx.send("The due date was not given in the right format: MM/DD/YY")
       return
    
    
    jsonFile = {
        "section_num": section_num,
        "assignment_info": assignment,
        "Due_Date": due_date,
        "Due_time": due_time
    }

    
    if(ctx.channel.id == cs1083ID):
        try:
            with open("cs1083.json", "a") as outfile:
                json_object = json.dumps(jsonFile, indent = 4)
                outfile.write(json_object)
            await ctx.send("Event added to calendar")
        except IOError:
            await ctx.send("There was a problem")        
    elif(ctx.channel.id == cs1714ID):
        try:
            with open("cs1714.json", "a") as outfile:
                json_object = json.dumps(jsonFile, indent = 4)
                outfile.write(json_object)
            await ctx.send("Event added to calendar")
        except IOError:
            await ctx.send("There was a problem")  
    elif(ctx.channel.id == cs3443ID):
        try:
            with open("cs3443.json", "a") as outfile:
                json_object = json.dumps(jsonFile, indent = 4)
                outfile.write(json_object)
            await ctx.send("Event added to calendar")
        except IOError:
            await ctx.send("There was a problem")  
    elif(ctx.channel.id == cs3424ID):
        try:
            with open("cs3424.json", "a") as outfile:
                json_object = json.dumps(jsonFile, indent = 4)
                outfile.write(json_object)
            await ctx.send("Event added to calendar")
        except IOError:
            await ctx.send("There was a problem")  
    else:
        await ctx.send("There is no calendar for this channel")
        
@bot.command(name='delete', help='Delete event from a calendar')
async def deleteEvent(ctx):
   
    if(ctx.channel.id == cs1083ID):
        await ctx.send("delete for channel 1083")
    elif(ctx.channel.id == cs1714ID):
        await ctx.send("delete for channel 1714")
    elif(ctx.channel.id == cs3443ID):
        await ctx.send("delete for channel 3443")
    elif(ctx.channel.id == cs3424ID):
        await ctx.send("delete for channel 3424")
    else:
        await ctx.send("There is no calendar for this channel")

@bot.command(name='list', help='List all events for a calendar')
async def ListAll(ctx):
    if(ctx.channel.id == cs1083ID):
        await ctx.send("list for channel 1083")
    elif(ctx.channel.id == cs1714ID):
        await ctx.send("list for channel 1714")
    elif(ctx.channel.id == cs3443ID):
        await ctx.send("list for channel 3443")
    elif(ctx.channel.id == cs3424ID):
        await ctx.send("list for channel 3424")
    else:
        await ctx.send("There is no calendar for this channel")

bot.run(TOKEN)
    
