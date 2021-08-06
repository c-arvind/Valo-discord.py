import json
import aiohttp
import asyncio
import webbrowser

async def cred_validate(username,tag):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.henrikdev.xyz/valorant/v1/account/{username}/{tag}') as r:
            data=await r.json()
            return data

async def live_match(username,tag):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.henrikdev.xyz/valorant/v1/live-match/{username}/{tag}') as r:
            data=await r.json()
            return data

async def mmr(username,tag,region):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.henrikdev.xyz/valorant/v2/mmr/{region}/{username}/{tag}') as r:
            data = (await r.json())["data"]
            return data['current_data']

async def mmr_history(username,tag,region):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.henrikdev.xyz/valorant/v1/mmr-history/{region}/{username}/{tag}') as r:
            data=(await r.json()) 
            return data


async def statistics(username,tag):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.tracker.gg/api/v2/valorant/standard/profile/riot/{username}%23{tag}", json={}) as r:
            data = await r.json()
            try:
                if data['errors'][0]['message']=='This profile is still private.':
                    webbrowser.open(f'https://tracker.gg/valorant/profile/riot/{username}%23{tag}/overview')
            except KeyError:
                user = data['data']["platformInfo"]["platformUserHandle"]
                avatarUrl = data['data']["platformInfo"]["avatarUrl"]

                stats = data['data']["segments"][0]["stats"]
                win_pct = stats["matchesWinPct"]["displayValue"]
                hs_pct = stats["headshotsPercentage"]["displayValue"]
                kd_ratio = stats["kDRatio"]["displayValue"]
                aces = stats["aces"]["displayValue"]
                time_played = stats["timePlayed"]["displayValue"]
                rank = stats["rank"]["metadata"]["tierName"]
                rankIconUrl = stats["rank"]["metadata"]["iconUrl"]

                DATA = dict(
                    user=user,
                    avatarUrl=avatarUrl,
                    win_pct=win_pct,
                    hs_pct=hs_pct,
                    kd_ratio=kd_ratio,
                    aces=aces,
                    time_played=time_played,
                    rank=rank,
                    rankIconUrl=rankIconUrl,
                )
                return DATA

                

    

