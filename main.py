import nextcord
import openai
import json
import sqlite3
import time
import os
import keys

from threading import Thread
from nextcord.ext import commands
from pathlib import Path

connection= sqlite3.connect("data.sqlite")
cursor= connection.cursor()

bot = commands.Bot(
	command_prefix="$",
	intents= nextcord.Intents.all()
)


bot.openai_api = keys.openai
openai.api_key = bot.openai_api

async def repeated_things():
	for cog in Path("cogs/").glob("*.py"):
		cog_name = cog.name.split(".")[0]
		bot.reload_extension(f"cogs.{cog_name}")
		print("Extension Reloaded:", cog_name)
	guild_count = 0
	guild_member_count = 0
	print("Guild counting started")
	guild_count_time = time.time()
	for guild in bot.guilds:
		guild_count += 1
		guild_member_count += guild.member_count
	await bot.change_presence(status="idle",activity=nextcord.Game(name=f"Watching {guild_count} server and {guild_member_count} member + {len(cursor.execute('select * from qoqnus_acc').fetchall())} QHP User 👀"))
	print(f"Guild counting completed in {time.time() - guild_count_time}s")

@bot.event
async def on_ready():
	print(f"Bot commands are ready in {time.time() - bot.started_time}s")
	await repeated_things()
	guild = bot.get_guild(1106102532553584642)
	role = guild.get_role(1106104227027226654)
	role2 = guild.get_role(1106104711561609348)
	print("Auto role started")
	auto_role_time = time.time()
	for i in guild.members:
		if i.bot and not role2 in i.roles:
			await i.add_roles(role2)
			await i.remove_roles(role)
		elif role in i.roles:
			await i.add_roles(role)
			await i.remove_roles(role2)
	print(f"Auto role completed in {time.time() - auto_role_time}s")
	print(f"Bot full loaded in {time.time() - bot.started_time}s")
		
@bot.event
async def on_message(message:nextcord.Message):
	if message.content.startswith(f"<@{bot.application_id}>"):
		async with message.channel.typing():
			message_content = message.content.split(f"<@{bot.application_id}>")[1]
			user = cursor.execute(f"""select * from qoqnus_acc where disid="{message.author.id}" """).fetchall()
			data_files_list = []
			for i in Path("gpt").iterdir():
				data_files_list += [int(i.name)]
			if len(user) != 0:
				user = user[0]
				if message.author.id in data_files_list:
					data = json.load(open(f"gpt/{message.author.id}", "r"))
					if data["enable"]:
						full_msg = data["message"] + [{"role":"user", "content":message_content}]
						response = openai.ChatCompletion.create(
							model="gpt-3.5-turbo",
							messages= full_msg,
							max_tokens=100,
							temperature=1.2
						)
						full_msg += [{"role": "assistant", "content": response.choices[0]["message"]["content"]}]
						with open(f"gpt/{message.author.id}", "w") as data:
							json.dump({"enable":True, "message":full_msg}, data)
						msg = response.choices[0]["message"]["content"]
						#await self.aroom_msg(msg, msg=message)
						await message.reply(msg)
						await repeated_things()
						return
			response = openai.ChatCompletion.create(
				model = "gpt-3.5-turbo",
				messages = [{"role":"user", "content": message_content}],
				max_tokens=100,
				temperature=1.2,
			)
			msg = response.choices[0]["message"]["content"]
			#await self.aroom_msg(msg, msg=message)
			await message.reply(msg)
	await repeated_things()

@bot.event
async def on_member_join(member:nextcord.Member):
	if member.guild.id == 1106102532553584642:
		guild = bot.get_guild(1106102532553584642)
		role = guild.get_role(1106104227027226654)
		role2 = guild.get_role(1106104711561609348)
	elif member.guild.id == 1133325266576474204:
		guild = bot.get_guild(1133325266576474204)
		role = guild.get_role(1133326245438947378)
		role2 = guild.get_role(1133326128178802698)
	if member.bot:
		await member.add_roles(role2)
	else:
		await member.add_roles(role)
			
	embed = nextcord.Embed()
	
	embed.set_author(name="Qoqnus master", icon_url="https://media.discordapp.net/attachments/1108286830773813300/1130185790060756992/-80trk6.jpg")
			
	embed.add_field(inline=False, name="به سرور {0} خوش آمدید".format(member.guild.name), value="این سرور تحت سرویس ققنوس بات میباشد")
	embed.add_field(inline=False, name="با ساخت اکانت ققنوس مستر:", value="")
	embed.add_field(inline=False, name="", value="از طریق کامند shop با قوق کوین خرید و فروش کنید")
	embed.add_field(inline=False, name="", value="هوش مصنوعی با قابلیت حفظ پیام ها(vip gpt)")
	embed.add_field(inline=False, name="", value="مدیریت اکانت و سرور از وبسایت(به زودی)")
	embed.add_field(inline=False, name="", value="امکانات بیشتر به زودی...")
	embed.add_field(inline=False, name="پس چرا نشستی داری به این پیام نگاه میکنی/:", value="سریع تر با کامند create-account اکانت خودتو بساز!!")
			
	await member.send(embed=embed)
	await repeated_things()

if __name__ == "__main__":
	bot.started_time = time.time()
	for cog in Path("cogs/").glob("*.py"):
		cog_name = cog.name.split(".")[0]
		bot.load_extension(f"cogs.{cog_name}")
		print("Extension Loaded:", cog_name)
	Thread(target=os.system, args=["python manage.py runserver 0.0.0.0:7367"]).start()
	bot.run(keys.token)
