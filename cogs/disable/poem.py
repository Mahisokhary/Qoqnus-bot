import requests
import nextcord

from nextcord.ext import commands
from nextcord import Interaction
from nextcord import slash_command

class poem(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@slash_command(name = "poem", description ="ارسال یکی از اشعار ایرانی")
	async def ping(self, ctx: Interaction):
		embed=nextcord.Embed(color=nextcord.Colour.yellow())
		embed.set_author(name="Powerd by ganjoor.net", icon_url="https://ganjoor.net/image/gdap.png")
		embed.add_field(name="درحال دریافت شعر...", value="", inline=False)		
		ctx_resonse = await ctx.response.send_message(embed=embed)
		try:
			r = requests.request(method="GET" ,url="https://api.ganjoor.net/api/ganjoor/poem/random").json()
			embed = nextcord.Embed(color=nextcord.Colour.green())
			embed.set_author(name="Powerd by ganjoor.net", icon_url="https://ganjoor.net/image/gdap.png")
			embed.add_field(name=r["fullTitle"], value=r["plainText"], inline=False)
			await ctx_resonse.edit(embed=embed)
		except:
			embed = nextcord.Embed(color=nextcord.Colour.red())
			embed.set_author(name="Powerd by ganjoor.net", icon_url="https://ganjoor.net/image/gdap.png")
			embed.add_field(name="متاسفانه خطایی رخ داد", value="", inline=False)
			await ctx_resonse.edit(embed=embed)

def setup(bot:commands.Bot):
    bot.add_cog(poem(bot))
