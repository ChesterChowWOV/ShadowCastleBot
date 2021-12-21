import discord
from discord.ext import commands

desc = """
This is a list of the commands.
Type `>help [command]` for more information on a command.\n\n
"""

class CommandsHelp(commands.HelpCommand):
  async def send_bot_help(self, mapping):
    ctx = self.context
    embed = discord.Embed(
      title="**__Help__**"
    )
    embed.description = desc
    h = []
    for cog, cmds in mapping.items():
      ch = "\n".join([f"`>{c.qualified_name} {c.signature}`" for c in cmds if not c.hidden])
      ch = "*_" + getattr(cog, "qualified_name", "Others") + "_*" + "\n" + ch
      h.append(ch)
    embed.description += "\n\n".join(h)
    await ctx.send(embed=embed)

  async def send_command_help(self, command):
    ctx = self.context
    embed = discord.Embed(
      title="Help for " + command.name
    )
    embed.add_field(name="Name",value=f"`{command.name}`")
    embed.add_field(name="Aliases",value=", ".join(f"`{a}`" for a in command.aliases) if command.aliases else "None")
    embed.add_field(name="Description", value=command.help or "N/A")
    embed.add_field(name="Usage",value=f"`>{command.qualified_name} {command.signature}`")
    await ctx.send(embed=embed)

def setup(bot):
  bot.help_command = CommandsHelp()