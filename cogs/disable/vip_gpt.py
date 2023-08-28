import nextcord
import sqlite3
import json
import os

from pathlib import Path
from nextcord.ext import commands
from nextcord import Interaction
from nextcord import slash_command

connection= sqlite3.connect("data.sqlite")
cursor= connection.cursor()

class vip_gpt(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@slash_command(name = "vip-gpt", description = "ثبت مکالمه ها با چت جی‌پی‌تی")
	async def vip_gpt(self, ctx: Interaction, turn_on:bool):
		data_files_list = []
		for i in Path("gpt").iterdir():
			data_files_list += [int(i.name)]
		qoqnus_acc = cursor.execute(f"""select * from qoqnus_acc where disid="{ctx.user.id}" """).fetchall()
		if len(qoqnus_acc) == 0:
			await ctx.response.send_message("لطفا ابتدا اکانت ققنوس بات بسازید")
			return 
		else:
			qoqnus_acc = qoqnus_acc[0]
		if turn_on:
			messages= []
			if ctx.user.id in data_files_list:
				if json.load(open(f"gpt/{ctx.user.id}", "r"))["enable"]:
					await ctx.response.send_message("شما از قبل این قابلیت را فعال کرده اید")
					return
				else:
					messages = json.load(open(f"gpt/{ctx.user.id}", "r"))["message"]
			else:
				os.system(f"touch gpt/{ctx.user.id}")
			with open(f"gpt/{ctx.user.id}", "w") as file:
				json.dump({"enable": True, "message": messages}, file)
				file.close()
			await ctx.response.send_message("جی‌پی‌تی اختصاصی با موفقیت فعال شد")
		else:
			data = json.load(open(f"gpt/{ctx.user.id}", "r"))
			data["enable"] = False
			with open(f"gpt/{ctx.user.id}", "w") as file:
				json.dump(data, file)
				file.close()
			await ctx.response.send_message("جی‌پی‌تی اختصاصی با موفقیت غیر فعال شد")

def setup(bot):
	bot.add_cog(vip_gpt(bot))
