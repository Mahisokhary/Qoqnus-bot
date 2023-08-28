import nextcord
import json
import os
import random

from pathlib import Path
from nextcord.ext import commands
from nextcord import Interaction
from nextcord import slash_command

class create_modal(nextcord.ui.Modal):
	def __init__(self, channel:nextcord.TextChannel):
		self.channel = channel
		super().__init__(title="ساخت گیو اوی")
		self.giveaway_name = nextcord.ui.TextInput(label="نام گیو اوی:", placeholder="جهت مدیریت گیو اوی")
		self.giveaway_title = nextcord.ui.TextInput(label="عنوان گیواوی:")
		self.giveaway_description = nextcord.ui.TextInput(label="توضیحات گیواوی:", style=nextcord.TextInputStyle.paragraph)
		self.giveaway_btn_txt = nextcord.ui.TextInput(label="دکمه گیو اوی:", placeholder="نوشته روی دکمه شرکت در گیپ اوی")
		self.giveaway_on_join = nextcord.ui.TextInput(label="پیام برای شرکت کننده:", placeholder="این نوشته بعد از شرکت در گیو اوی نمایش داده میشود", style=nextcord.TextInputStyle.paragraph)
		self.giveaway = [
			self.giveaway_name,
			self.giveaway_title,
			self.giveaway_description,
			self.giveaway_btn_txt,
			self.giveaway_on_join
		]
		for item in self.giveaway:
			self.add_item(item)
		#self.add_item(nextcord.ui.TextInput(label="لینک تصویر گیو اوی:", placeholder="https://exemple.com/test.png"))
	async def callback(self, ctx:Interaction):
		allowed= "abcdefghijklmonpqrstuvwxyz"
		for i in self.giveaway_name.value:
			if not i in allowed:
				await ctx.response.send_message("نام گیو اوی میتواند تنها شامل a-z باشد", ephemeral=True)
				return 
		message = await self.channel.send(".")
		data = {
			"name": self.giveaway_title.value,
			"description": self.giveaway_description.value,
			"btn-text": self.giveaway_btn_txt.value,
			"on-join-msg": self.giveaway_on_join.value,
			"ch": self.channel.id,
			"msg": message.id,
		}
		paths = [
			{"n": "data/", "d": True},
			{"n": f"data/{self.channel.guild.id}/", "d": True},
			{"n": f"data/{self.channel.guild.id}/giveaways/", "d": True},
			{"n": f"data/{self.channel.guild.id}/giveaways/{self.giveaway_name.value}/", "d": True},
			{"n": f"data/{self.channel.guild.id}/giveaways/{self.giveaway_name.value}/data", "d": False},
			{"n": f"data/{self.channel.guild.id}/giveaways/{self.giveaway_name.value}/joined/", "d":True}
		]
		base_dir = f"data/{self.channel.guild.id}/giveaways/{self.giveaway_name.value}/"
		for path in paths:
			if not Path(path["n"]).exists():
				if path["d"]:
					os.system(f"mkdir {path['n']}")
				else:
					os.system(f"touch {path['n']}")
		json.dump(data, open(base_dir + "data", "w"))
		embed = nextcord.Embed(title=data["name"])
		embed.add_field(inline=False, name="توضیحات:", value=data["description"])
		
		class view(nextcord.ui.View):
			def __init__(self):
				super().__init__()
			@nextcord.ui.button(label=data["btn-text"], style=nextcord.ButtonStyle.green)
			async def btn(self, btn, ctx:Interaction):
				if Path(base_dir + f"joined/{ctx.user.id}").exists():
					await ctx.response.send_message("شما از قبل ثبت نام کرده اید✅", ephemeral=True)
					return
				os.system(f"touch {base_dir}joined/{ctx.user.id}")
				await ctx.response.send_message(data["on-join-msg"], ephemeral=True)
		
		await message.edit(content="**گیو اوی:**", embed=embed, view=view())
		await ctx.response.send_message("گیو اوی با موفقیت ساخته شد✅\ngiveaway_name={0}".format(self.giveaway_name.value), ephemeral=True)
class giveaway(commands.Cog):
	def __init__(self, bot:commands.Bot):
		self.bot = bot
	
	@slash_command(name = "giveaway", description = "گیواوی")
	async def giveaway(self, ctx: Interaction):
		pass
	
	@giveaway.subcommand(name="create", description= "ساخت گیو اوی(مخصوص ادمین ها)")
	async def giveaway_create(self, ctx: Interaction, channel:nextcord.TextChannel):
		if ctx.user.id == ctx.guild.owner_id:
			await ctx.response.send_modal(create_modal(channel))
		else:
			await ctx.response.send_message("این کامند فقط برای دارنده سرور است", ephemeral=True)
	
	@giveaway.subcommand(name="delete", description="حذف گیو اوی(مخصوص ادمین ها)")
	async def giveaway_delete(self, ctx:Interaction, giveaway_name:str, delete_give_away_msg:bool=False):
		if ctx.user.id == ctx.guild.owner_id:
			try:
				data = json.load(open(f"data/{ctx.guild.id}/giveaways/{giveaway_name}/data"))
				if delete_give_away_msg:
					await self.bot.get_channel(data["ch"]).get_partial_message(data["msg"]).delete()
				os.system(f"rm -rf data/{ctx.guild.id}/giveaways/{giveaway_name}/")
				await ctx.response.send_message("گیو اوی با موفقیت حذف شد✅", ephemeral=True)
			except Exception as e:
				print(e)
				await ctx.response.send_message("گیو اوی پیدا نشد", ephemeral=True)
		else:
			await ctx.response.send_message("این کامند فقط برای دارنده سرور است", ephemeral=True)
		
	@giveaway.subcommand(name="throw", description="برگزاری گیو اوی(مخصوص ادمین ها)")
	async def giveaway_throw(self, ctx:Interaction, giveaway_name:str, times:int=1):
		if ctx.user.id == ctx.guild.owner_id:
			try:
				for i in range(times):
					data = json.load(open(f"data/{ctx.guild.id}/giveaways/{giveaway_name}/data"))
					joined = [x.name for x in Path(f"data/{ctx.guild.id}/giveaways/{giveaway_name}/joined/").iterdir()]
					try:
						selected = random.choice(joined)
					except:
						await ctx.response.send_message("هیچ کس تو گیو اوی شرکت نکرده):", ephemeral=True)
						return 
					msg = ctx.guild.get_channel(data["ch"]).get_partial_message(data["msg"])
					await msg.reply("{0} برنده گیو اوی شد🎉🎉🎉".format(f"<@{selected}>"))
					await ctx.response.send_message("✅", ephemeral=True)
			except Exception as e:
				print(e)
				await ctx.response.send_message("گیو اوی انتخاب شده یافت نشد", ephemeral=True)
		else:
			await ctx.response.send_message("این کامند فقط برای دارنده سرور است", ephemeral=True)
	
def setup(bot:commands.Bot):
	bot.add_cog(giveaway(bot))
