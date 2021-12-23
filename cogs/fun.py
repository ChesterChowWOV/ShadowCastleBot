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
        await ctx.send("".join(all_chars))

    @commands.command()
    async def reverse(self, ctx, *, text):
      await ctx.send(text[::-1])

    @commands.group(invoke_without_command=True)
    async def tag(self, ctx, *, name):
        with open("data/tags.json") as f:
            data = json.load(f)
            tag_content = data.get(name.lower(), None)
        if tag_content is None:
            await ctx.reply(f"Tag \"{name}\" not found.", delete_after=5)
        else:
            await ctx.send(tag_content["content"])

    @tag.command()
    async def create(self, ctx, name, *, content):
        with open("data/tags.json") as f:
            data = json.load(f)
        if name.lower() in data.keys():
          return await ctx.send("This tag already exists.")
        data.update({name.lower(): {"author": ctx.author.id, "content": content}})
        with open("data/tags.json", "w") as f:
            json.dump(data, f, indent=2)
        await ctx.send("\N{OK HAND SIGN}")

    @tag.command()
    async def edit(self, ctx, name, *, content):
      with open("data/tags.json") as f:
        data = json.load(f)
      tag_content = data.get(name.lower(), None)
      if tag_content is None:
        return await ctx.reply(f"Tag \"{name}\" not found.", delete_after=5)
      if tag_content["author"] != ctx.author.id:
        return await ctx.reply(f"You don't own the tag \"{name}\".", delete_after=5)
      data[name.lower()] = {
        "author": tag_content["author"],
        "content": content
      }
      with open("data/tags.json", "w") as f:
        json.dump(data, f, indent=2)


def setup(bot):
    bot.add_cog(Fun(bot))
