import discord
from discord.ext import commands
import database as db
import aiohttp
from api import *
import re


token = open("token.txt","r").readline()
client = discord.Client()
bot = commands.Bot(command_prefix="v.")
@bot.event
async def on_ready():
    print("Bot connected.")

@bot.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("Wrong command format")
        #await ctx.message.delete()

@bot.command()
async def link(ctx,username,tag):
    tag=re.sub("^#",'',tag)
    data= await cred_validate(username,tag)
    if data['status']=='200':
        db.set_record(ctx.message.author.id,username,tag,data['data'])
        await ctx.send(ctx.message.author.mention," you are linked :white_check_mark:")
    elif data['status']=='404':
        return data['message']
    else:
        await ctx.send("error...contact me") 
    #db.set_record(ctx.message.author.id,username,tag)
    #db.get_record(ctx.message.author.id)


@bot.command()
async def rank(ctx, member: discord.Member=None):
    if member is None:
        member = ctx.message.author
    print(type(member.id))
    await ctx.send(member)

@bot.command()
async def live(ctx,member:discord.Member):
    #data=await live_match()
    db.get_record(member.id)
    await ctx.send("done")


bot.run(token)

