import nextcord
import openai
import asyncio

from nextcord.ext import commands
from nextcord import Interaction
from nextcord import slash_command

class dalle(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.wait = []
	
	@slash_command(name = "dalle", description = "تبدیل متن به تصویر با دال-ای ۲")
	async def dalle(self, ctx: Interaction, prompt:str):
		if ctx.user.id in self.wait:
			await ctx.response.send_message("برای استفاده مجدد از کامند باید 2دقیقه صبر کنید(گرونهههه)", ephemeral=True)
			return 
		embed = nextcord.Embed(color=nextcord.Colour.yellow())
		embed.set_author(name=ctx.user.name, icon_url=ctx.user.avatar.url)
		embed.add_field(name="دستور: {0}".format(prompt), value="درحال ساخت تصویر...", inline=False)
		ctx_response = await ctx.response.send_message(embed=embed)
		try:
			vip = [
				1019484919195521034, #Qoqnus master
			]
			if ctx.user.id in vip:
				size = "1024x1024"
			else:
				size = "256x256"
			openai.api_key = self.bot.openai_api
			response = openai.Image.create(
			    prompt= prompt,
			    n=1,
	 		   size=size
				)
			embed = nextcord.Embed(color=nextcord.Colour.green())
			embed.set_author(name=ctx.user.name, icon_url=ctx.user.avatar.url)
			embed.add_field(inline=True, name="دستور:{0}".format(prompt), value="")
			embed.set_image(url=response["data"][0]["url"])
			await ctx_response.edit(embed=embed)
		except Exception as e:
			#print(e)
			embed = nextcord.Embed(color=nextcord.Colour.red())
			embed.set_author(name=ctx.user.name, icon_url=ctx.user.avatar.url)
			embed.add_field(inline=True, name="دستور:{0}".format(prompt), value="خطا رخ داد!")
			embed.add_field(inline=True, name="توضیحات خطا:", value=e)
			await ctx_response.edit(embed=embed)
		self.wait += [ctx.user.id]
		x = len(self.wait)
		await asyncio.sleep(120)
		self.wait[x-1] = 0

def setup(bot:commands.Bot):
	bot.add_cog(dalle(bot))
