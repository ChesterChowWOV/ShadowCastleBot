import discord
from discord.ext import commands
import typing
import json

class Management(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @commands.command()
  async def membercount(self, ctx):
    return await ctx.send(embed=discord.Embed(
      title="Member Count",
      description=f"Total {ctx.guild.member_count} members;\nHumans: {len([m for m in ctx.guild.members if not m.bot])};\nBots: {len([m for m in ctx.guild.members if m.bot])}."
    ))
  @commands.command()
  @commands.has_permissions(ban_members=True)
  async def ban(self, ctx, user: typing.Union[discord.Member, discord.User], delete: typing.Optional[bool]=True, *, reason: typing.Optional[str]=None):
    await ctx.guild.ban(user, reason=reason, delete_message_days=7 if delete else 0)
    await ctx.send(ctx.author.mention+": \N{OK HAND SIGN} Banned "+str(user)+".")

  @commands.command()
  @commands.has_permissions(ban_members=True)
  async def kick(self, ctx, member: typing.Union[discord.Member, discord.User], *, reason: typing.Optional[str]=None):
    await ctx.guild.kick(member, reason=reason)
    await ctx.send(ctx.author.mention+": \N{OK HAND SIGN} Kicked "+str(member)+".")
  
  @commands.command()
  @commands.is_owner()
  async def set(self, ctx, channel: discord.TextChannel):
    self.bot.one_word_story = channel.id
    await ctx.ok()
  @commands.command(aliases=["bl"])
  @commands.is_owner()
  async def blacklist(self, ctx, user: discord.User, mode: typing.Optional[bool] = True):
    with open("data/blacklist.json", "r") as f:
      bl = json.load(f)
    if mode:
      bl.append(user.id)
    else:
      bl.remove(user.id)
    with open("data/blacklist.json", "w") as f:
      json.dump(bl, f)
    await ctx.send("\N{OK HAND SIGN}")

def setup(bot):
  bot.add_cog(Management(bot))