import discord
from discord.ext import commands
import json

class Fun(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def wide(self, ctx, *, text):
    all_chars = []
    for char in text:
      all_chars.append(char)
      all_chars.append(" ")
    await ctx.send(
      "".join(all_chars)
    )

  @commands.group(invoke_without_command=True)
  async def tag(self, ctx, *, name):
    with open("data/tags.json") as f:
      data = json.load(f)
      tag_content = data.get(name, None)
    if tag_content is None:
      await ctx.reply(f"Tag \"{name}\" not found.", delete_after=5)
    else:
      await ctx.send(tag_content["content"])
  
  @tag.command()
  async def create(self, ctx, name, *, content):
    with open("data/tags.json") as f:
      data = json.load(f)
    data.update({
      name: {
        "author":ctx.author.id,
        "content":content
      }
    })
    with open("data/tags.json", "w") as f:
      json.dump(data, f)
    await ctx.send("\N{OK HAND SIGN}")

def setup(bot):
  bot.add_cog(Fun(bot))