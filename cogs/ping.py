import nextcord

from nextcord.ext import commands
from nextcord import Interaction
from nextcord import slash_command

class ping(commands.Cog):
	def __init__(self, bot:commands.Bot):
		self.bot = bot
	
	@slash_command(name = "ping", description = "نمایش پینگ ققنوس بات")
	async def ping(self, ctx: Interaction):
		embed=nextcord.Embed()
		embed.add_field(name="پونگ🏓😃", value="پینگ ققنوس بات {0}میلی ثانیه هستش".format(round(self.bot.latency * 1000, 0)), inline=False)
		await ctx.response.send_message( embed = embed, ephemeral= False)
		
		

def setup(bot:commands.Bot):
	bot.add_cog(ping(bot))
