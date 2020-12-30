import random
import discord
import urllib
import secrets
import asyncio
import aiohttp
import re
import requests
import random
import json

from io import BytesIO
from discord.ext import commands
from utils import lists, permissions, http, default, argparser


class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")

    @commands.command()
    async def stats(self, ctx, steamId):
        file_name = random.randint(1000,9999)

        profile = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=A70902E029FC4EB4B0AD229444F30B22&steamids=" + steamId)
        player = requests.get("http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=252490&key=A70902E029FC4EB4B0AD229444F30B22&steamid=" + steamId)
        profileJson = profile.json()
        playerData = player.json()

        for profile in profileJson.values():
            for player in profile.values():
                profile_name = player[0]['personaname']
                profile_avatar = player[0]['avatar']

        playerStats = playerData['playerstats']
        print(profile_avatar)

        for stat in playerStats['stats']:
            if(stat['name'] == 'kill_player'):
                stat_playerKills = stat['value']

            if(stat['name'] == 'deaths'):
                deaths = stat['value']

            if(stat['name'] == 'death_suicide'):
                death_suicide = stat['value']

            if(stat['name'] == 'death_fall'):
                death_fall = stat['value']

            if(stat['name'] == 'death_entity'):
                death_entity = stat['value']

            if(stat['name'] == 'death_bear'):
                death_bear = stat['value']

            if(stat['name'] == 'bullet_hit_player'):
                stat_bulletHitPlayer = stat['value']

            if(stat['name'] == 'bullet_fired'):
                stat_bulletFired = stat['value']

            if(stat['name'] == 'headshot'):
                stat_headshots = stat['value']

        hs_percentage = (stat_bulletHitPlayer / stat_headshots)

        stat_playerDeaths = (deaths - death_suicide - death_fall - death_entity - death_bear)

        stat_kd = (stat_playerKills / stat_playerDeaths)
        stat_kd = round(stat_kd, 2)

        if(stat_kd < 1 ):
            skill = 'Bot'
        elif(stat_kd > 1 and stat_kd < 2):
            skill = 'Good'
        elif(stat_kd > 2 and stat_kd < 3):
            skill = 'Amazing'
        else:
            skill = 'GOD'

        embed=discord.Embed(title='Rust Stats For: ' + profile_name)
        embed.set_thumbnail(url=profile_avatar)
        embed.add_field(name='Kills', value=stat_playerKills, inline=True)
        embed.add_field(name='Deaths', value=stat_playerDeaths, inline=True)
        embed.add_field(name='K/D', value=stat_kd, inline=True)
        embed.add_field(name='Skill', value=skill, inline=True)
        embed.set_footer(text="Rust Stats are gathered using the Steam API, Bot By @Carbine#6969")


        print('Requesting Stats: http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=252490&key=A70902E029FC4EB4B0AD229444F30B22&steamid=' + steamId)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Stats(bot))
