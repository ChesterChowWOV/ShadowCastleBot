from online import start
from discord.ext import commands, tasks
from discord_components import *
import discord
import os
import asyncio
import json
import logs
import traceback
import sys
import textwrap
import io
from contextlib import redirect_stdout

file = open('data/prefixes.json')
prefixes = json.load(file)
file.close()

def get_prefix(bot, msg):
  if msg.guild.id in prefixes:
    return prefixes[f"{msg.guild.id}"]
  return '>'

with open("data/blacklist.json") as f:
  blacklist = json.load(f)

class VibeBot(commands.Bot):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
  
  async def get_context(self, message, *, cls=None):
    return await super().get_context(message, cls=cls or Context)

bot = VibeBot(
  command_prefix=get_prefix, 
  case_insensitive=True,
  intents=discord.Intents.all(),
  allowed_mentions=discord.AllowedMentions.none()
  
)
bot.one_word_story = 923587278339702784

class Context(commands.Context):
  async def ok(self):
    await self.send("\N{OK HAND SIGN}")

ignored_cogs = []
for fn in os.listdir("./cogs"):
  if fn.endswith(".py"):
    if fn[:-3] in ignored_cogs:
      pass
    else:
      bot.load_extension("cogs."+fn[:-3])
      logs.green("Loaded extension:", fn)
bot.load_extension("helpcmd")

@bot.check
async def blacklist_check(ctx):
  return False if ctx.author.id in blacklist else True

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

@bot.listen()
async def on_message(msg):
  if msg.author.bot: return
  if msg.channel.id != bot.one_word_story: return
  length = len(msg.content.split(" "))
  if length != 1:
    return await msg.reply(f"Hey {msg.author.display_name}, you sent {length} words! This channel is a one word story channel, so you can only use one word to continue the last word's story.", components=[[Button(label="Delete my message", style=ButtonStyle.green), Button(label="Ignore warning", style=ButtonStyle.red)]])

@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
    return
  if isinstance(error, (commands.NotOwner, commands.MissingPermissions, commands.MissingAnyRole, commands.CheckFailure)):
    return await ctx.send("Hey, you don't have permissions to use this command.")
  if isinstance(error, commands.MissingRequiredArgument):
    return await ctx.reply(f"You missed a required parameter `{error.param.name}`.")
  try:
    raise error
  except Exception as e:
    await bot.owner.send(
      f"`{ctx.message.content}`\n{ctx.author}\n\n\n```py\n{traceback.format_exc()}```"
    )

@bot.listen()
async def on_button_click(res):
  #print(res.message.reference)
  if res.message.reference is None:
    return
  if res.component.label == "Ignore warning":
    return await res.message.delete()
  message = await res.channel.fetch_message(res.message.reference.message_id)
  
  await message.delete()
  await res.message.delete()

def cleanup_code(content):
  """Automatically removes code blocks from the code."""
        # remove ```py\n```
  if content.startswith('```') and content.endswith('```'):
    return '\n'.join(content.split('\n')[1:-1])
  return content.strip('` \n')

@bot.command(hidden=True, name='eval')
@commands.is_owner()
async def _eval(ctx, *, body: str):
  env = {
    'bot': bot,
    'ctx': ctx,
    'channel': ctx.channel,
    'author': ctx.author,
    'guild': ctx.guild,
    'message': ctx.message
  }

  env.update(globals())

  body = cleanup_code(body)
  stdout = io.StringIO()

  to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

  try:
    exec(to_compile, env)
  except Exception as e:
    return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

  func = env['func']
  try:
    with redirect_stdout(stdout):
      ret = await func()
  except Exception as e:
    value = stdout.getvalue()
    await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
  else:
    value = stdout.getvalue()
    try:
      await ctx.message.add_reaction('\u2705')
    except:
      pass

    if ret is None:
      if value:
        await ctx.send(f'```py\n{value}\n```')
    else:
      await ctx.send(f'```py\n{value}{ret}\n```')

@tasks.loop(seconds=20)
async def keep_chat_alive():
  await (bot.get_channel(921277195303927821)).send("Keeping the chat alive")

@keep_chat_alive.before_loop
async def wait():
  await bot.wait_until_ready()

# keep_chat_alive.start()
start()
bot.run(os.environ["TOKEN"])