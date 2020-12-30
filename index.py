import os
import discord
import asyncio
import requests
import datetime

from utils import default
from utils.data import Bot, HelpFormat
from discord.ext import commands, tasks

config = default.get("config.json")

print("Logging in...")

bot = Bot(
    command_prefix=config.prefix, prefix=config.prefix,
    owner_ids=config.owners, command_attrs=dict(hidden=True),
    help_command=HelpFormat(),
    intents=discord.Intents(  # kwargs found at https://discordpy.readthedocs.io/en/latest/api.html?highlight=intents#discord.Intents
        guilds=True, members=True, messages=True, reactions=True, voice_states = True
    )
)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

    game = discord.Game("Rust Stats")
    await bot.change_presence(status=discord.Status.online, activity=game)

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")

try:
    bot.run(config.token)
except Exception as e:
    print(f'Error when logging in: {e}')
