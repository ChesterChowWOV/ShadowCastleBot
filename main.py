from online import start
from discord.ext import commands
from discord_components import *
import discord
import os
import asyncio
import json
import logs
import traceback

file = open('data/prefixes.json')
prefixes = json.load(file)
file.close()

def get_prefix(bot, msg):
  if msg.guild.id in prefixes:
    return prefixes[f"{msg.guild.id}"]
  return '>'

bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True,intents=discord.Intents.all())

ignored_cogs = []
for fn in os.listdir("./cogs"):
  if fn.endswith(".py"):
    if fn[:-3] in ignored_cogs:
      pass
    else:
      bot.load_extension("cogs."+fn[:-3])
      logs.green("Loaded extension:", fn)
bot.load_extension("helpcmd")

@bot.event
async def on_ready():
  DiscordComponents(bot)
  logs.blue(f"Logged in as {bot.user}.")
  bot.owner = bot.get_user(788274635871092777)

@bot.command(hidden=True)
@commands.is_owner()
async def reload(ctx, ext):
  bot.reload_extension(ext)
  await ctx.send("\N{OK HAND SIGN}")


@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
    return
  await bot.owner.send(
    f"```py\n{traceback.format_exc()}```"
  )
start()
bot.run(os.environ["TOKEN"])