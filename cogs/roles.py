from discord.ext import commands
from discord_components import *
import discord
import os
import time
import asyncio
import json

def owner_or_perms(**perms):
    original = commands.has_permissions(**perms).predicate
    async def extended_check(ctx):
        if ctx.guild is None:
            return False
        return await commands.is_owner().predicate(ctx) or await original(ctx)
    return commands.check(extended_check)

    
class Roles(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(aliases=["br","buttonroles","button-roles"])
  @owner_or_perms(manage_guild=True)
  async def button_role(self, ctx):
    same_check = lambda m: ctx.channel.id == m.channel.id and ctx.author.id == m.author.id
    await ctx.send("Hello. Which channel would you want to make the button roles?")
    channel = await self.bot.wait_for("message",check=same_check)
    try:
      channel = await commands.TextChannelConverter().convert(ctx, channel.content)
    except commands.ChannelNotFound:
      await ctx.send("Sorry, but you provided an invalid channel. Please run the command to try again.")
      return
    perms = channel.permissions_for(ctx.guild.me)
    if not (perms.send_messages and perms.add_reactions):
      await ctx.send("Hmm, why can't I send a message or add reactions? Please give me proper pemissions in the channel and run this command again.")
      return
    await ctx.send(f"Alright, the channel is {channel.mention}. Now what should the message say? Type cancel to exit the process.")
    msg = await self.bot.wait_for("message", check=same_check)
    msg = msg.content
    if msg.lower() == "cancel":
      return
    await ctx.send("Thanks. Now, please send the roles.\n\nType \"done\" to finish the process.")
    roles = []
    while 1:
      rm = await self.bot.wait_for("message",check=same_check)
      if rm.content.lower() == "done":
        break
      try:
        r = await commands.RoleConverter().convert(ctx, rm.content)
        await rm.add_reaction("\N{WHITE HEAVY CHECK MARK}")
        roles.append(r)
      except commands.RoleNotFound:
        await ctx.send("Sorry, but you provided an invalid role. Please send another role.")
    await ctx.send("Done.")
    await channel.send(msg,components=[[Button(label=ro.name, style=ButtonStyle.blue, id=str(ro.id)) for ro in roles]])

  @commands.Cog.listener()
  async def on_button_click(self, res):
    try:
      role = discord.utils.get(res.guild.roles, id=int(res.component.id))
    except ValueError:
      return
    if role is not None:
      if role.id in [r.id for r in res.user.roles]:
        await res.user.remove_roles(role)
        await res.respond(content=f"Successfully removed your role {role.name}.")
      else:
        await res.user.add_roles(role)
        await res.respond(content=f"Successfully gave you the role {role.name}.")
      #new_label = res.component.label[:-3]
      #new_label += f"({len(role.members)})"
      #await res.message.edit(components=[res.message.components])


def setup(bot):
  bot.add_cog(Roles(bot))