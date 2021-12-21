import discord
from discord.ext import commands
import typing

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
  async def ban(self, ctx, mem: typing.Union[discord.Member, discord.User], delete: typing.Optional[bool]=True, *, reason: typing.Optional[str]=None):
    await ctx.guild.ban(mem, reason=reason, delete_message_days=7 if delete else 0)
    await ctx.send(ctx.author.mention+": \N{OK HAND SIGN} Banned "+str(mem)+".")

  
def setup(bot):
  bot.add_cog(Management(bot))