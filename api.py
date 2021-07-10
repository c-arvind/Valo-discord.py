import json
import aiohttp
import asyncio

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
        