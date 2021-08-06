import discord
from discord.ext import commands
import database as db
import aiohttp
from api import *
import re
import datetime
from util import *
from matplotlib import pyplot as plt
import numpy as np
from graph import *
import io


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
async def link(ctx,username,itag):
    tag=re.sub("^#",'',itag)
    data= await cred_validate(username,tag)
    if data['status']=='200':
        db.set_record(ctx.message.author.id,username,tag,data['data'])
        await ctx.send(f"{ctx.message.author.mention} you are linked ☑")
    elif data['status']=='404':
        await ctx.send(data['message'])
    else:
        await ctx.send(data['message']) 
    #db.set_record(ctx.message.author.id,username,tag)
    #db.get_record(ctx.message.author.id)


@bot.command()
async def rank(ctx, member: discord.Member=None):
    if member is not None:
        await ctx.send(f"{member.mention} hello")
    else:
        await ctx.send(ctx.message.author.mention)
    

''' 
@bot.command()
async def status(ctx, region):
    if region in ('eu', 'ap', 'na', 'kr'):
'''

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
                    sym="✅"
                else:
                    sym="❌"
                
                embed=discord.Embed(title=data2['current_state'], description=f"custom {sym}")
                embed.set_thumbnail(url=gamemode_icons[gamemode])
                embed.set_author(name="{} #{}".format(details['display_name'],details['tag'])) 
                embed.add_field(name="game mode", value=f"{gamemode} {score}", inline=True)
                embed.add_field(name='\b', value='\b',inline=True)
                embed.add_field(name="MAP", value=data2['map'], inline=True)
                #embed.timestamp = datetime.datetime.utcnow()
                embed.set_footer(url="https://https://media.valorant-api.com/maps/7eaecc1b-4337-bbf6-6ab9-04b8f06b3319/listviewicon.png")
                await ctx.send(embed=embed)
                         
        else:
            await ctx.send("SERVER ERROR")

@bot.command()
async def stats(ctx,member:discord.Member=None):

    if member is None:
        member=ctx.message.author
    details=db.get_record(member.id)
    if details is None:
        await ctx.send(f'{member.mention} has not linked their account')
    else:
        p1=await statistics(details['display_name'],details['tag'])
        p1['acc_level']=details['details']['account_level']
        p1mmr=await mmr(details['display_name'],details['tag'],details['details']['region'])

        if p1mmr['games_needed_for_rating']!=0:
            rank="unranked"
            description=""
        else:
            rank=p1mmr['currenttierpatched']
            description =  f"**{p1mmr['ranking_in_tier']}/100** RR | **{p1mmr['elo']}** ELO"
        embed = discord.Embed(title=rank, description=description)
        embed.set_thumbnail(url=p1["rankIconUrl"])
        embed.set_author(name=p1['user'], icon_url=p1["avatarUrl"])
        embed.add_field(name="K/D Ratio", value=p1["kd_ratio"])
        embed.add_field(name="\u200b", value="\u200b")
        embed.add_field(name="Aces", value=p1["aces"])
        
        embed.add_field(name="Headshot %", value=p1["hs_pct"])
        embed.add_field(name="\uFEFF", value="\uFEFF")
        embed.add_field(name="Win %", value=p1["win_pct"])
        embed.add_field(name="Time Played", value=p1["time_played"])
        embed.add_field(name="\u200b", value="\u200b")
        embed.add_field(name="Account Level",value=p1['acc_level'])
        await ctx.send(embed=embed)
 
@bot.command()
async def matches(ctx,member:discord.Member=None):

    if member is None:
        member=ctx.message.author
    details=db.get_record(member.id)
    if details is None:
        await ctx.send(f'{member.mention} has not linked their account')
    else:
        p1=await mmr_history(details['display_name'],details['tag'],details['details']['region'])
        if p1 is None:
            await ctx.send("NOT PLACED")
        else:
            ratings=[]
            for match in p1['data']:
                ratings.append(match['mmr_change_to_last_game'])
            embed = discord.Embed(title=f"{details['display_name']}'s match history", description=f"Current rank: **{p1['data'][0]['currenttierpatched']}**") 

            embed.add_field(name="Last game played",value=p1['data'][0]['date'])  
            #embed.add_field(name="matches",value=ratings)
            plot(ratings)
            image=discord.File("saved_figure.png",filename="saved_figure.png")
            embed.set_image(url=f"attachment://saved_figure.png")
            await ctx.send(file=image,embed=embed)

@bot.command()
async def plot_test(ctx, *args):
    x = args
    try:
        image = discord.File("test.png")
        plt.bar(np.arange(len(x)), x)
        plt.savefig("test.png")
        plt.close()
        await ctx.send(file=image)
    except Exception as e:
        print(e)
              
bot.run(token)

