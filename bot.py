import discord
from discord.ext import commands
import database as db
import aiohttp
from api import *
import re
import datetime


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
        await ctx.send(f"{ctx.message.author.mention} you are linked :white_check_mark:")
    elif data['status']=='404':
        await ctx.send(data['message'])
    else:
        await ctx.send(data['message']) 
    #db.set_record(ctx.message.author.id,username,tag)
    #db.get_record(ctx.message.author.id)


@bot.command()
async def rank(ctx, member: discord.Member=None):
    if member is None:
        member = ctx.message.author
    await ctx.send(f"{member.mention} hello sir")

@bot.command()
async def status(ctx, region):
    if region in ('eu', 'ap', 'na', 'kr'):
        await ctx.send

@bot.command()
async def live(ctx,member:discord.Member):
    details=db.get_record(member.id)
    if details is None:
        await ctx.send(f'{member.mention} has not linked their account')
    else:
        data=await live_match(details['display_name'],details['tag'])
        if 'message' in data: 
            await ctx.send(data['message'])
        elif 'data' in data:
            embed=discord.Embed(title="")
            gamemode=""
            iscustom="false"
            data2=data['data']
            #await ctx.send(data['data']['current_selected_gamemode'])   
            if data2['current_state']=="MENUS":
                if data2['current_selected_gamemode']=="":
                    gamemode="custom"
                    iscustom="true"
                elif data2['current_selected_gamemode']=="ggteam":
                    gamemode="spike rush"
                else:
                    gamemode=data2['current_selected_gamemode']
                embed=discord.Embed(title="MENUS")
                embed.set_author(name="{} #{}".format(details['display_name'],details['tag']))
                embed.add_field(name="game mode", value=gamemode, inline=True)
                embed.add_field(name="party size", value=data2['party_size'], inline=True)
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_footer(text='\u200b')
                await ctx.send(embed=embed)
            else:
                score=f"[{data2['score_ally_team']}:{data2['score_enemy_team']}]"
                if data2["custom_game"]=="true":
                    sym="::white_check_mark:"
                else:
                    sym=":x:"
                
                embed=discord.Embed(title=data2['current_state'], description=f"custom {sym}")
                embed.set_author(name="{} #{}".format(details['display_name'],details['tag'])) 
                embed.add_field(name="game mode", value=f"{gamemode} {score}", inline=True)
                embed.add_field(name='\b', value='\b',inline=True)
                embed.add_field(name="MAP", value=data2['map'], inline=True)
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_footer(text='\u200b')
                await ctx.send(embed=embed)
                
                
        else:
            await ctx.send("SERVER ERROR")

bot.run(token)

