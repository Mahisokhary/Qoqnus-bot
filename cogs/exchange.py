import nextcord
import asyncio
import sqlite3

from typing import Literal
from nextcord.ext import commands
from nextcord import Interaction
from nextcord import slash_command

connection = sqlite3.connect('exchange.sqlite')
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS exchange (
        exchange_channel integer,
		exchange_log_channel integer,
		exchange_admin_role integer,
		member_limit integer,
		name varchar(255),
		mention_limit integer,
		banner integer,
		time integer,
		guild_id integer,
		mention varchar(255),
		num_id integer
    )
""")

"""
insert into qoqnus_acc values
(
exchange_channel,
exchange_log_channel,
exchange_admin_role,
member_limit,
name,
mention_limit,
banner,
time,
guild_id,
mention,
num_id
)
"""

class exchange2(nextcord.ui.Modal):
	def __init__(self, server, bot, private) -> None:
		self.private = private
		self.server = server
		self.bot = bot
		super().__init__(title="اکسچنج با {0}".format(self.server["name"]))
		self.banner = nextcord.ui.TextInput(label="بنر سرورتون:", placeholder="بنر، تبلیغ یا هرچی که بهش میگی", style=nextcord.TextInputStyle.paragraph)
		self.guild_count = nextcord.ui.TextInput(label="تعداد ممبر های سرورتون:", placeholder="اعداد انگلیسی، مثال: 100", style=nextcord.TextInputStyle.short)
		self.add_item(self.banner)
		self.add_item(self.guild_count)
	async def callback(self, ctx:Interaction):
		banner = self.banner.value
		try:
			member_count = int(self.guild_count.value)
		except:
			await ctx.response.send_message("ورودی تعداد ممبر های سرور صحیح نیست", ephemeral=self.private)
			return
		if member_count < self.server["mention-limit"]:
			banner = banner.replace("@here", ".")
			banner = banner.replace("@everyone", ".")
		if self.server["mention"] != "":
			banner = banner.replace("@here", ".")			
			banner = banner.replace("@everyone", ".")
			banner += f"\nAuto tag: {self.server['mention']}"
		if member_count >= self.server["member-limit"]:
			channel = self.bot.get_guild(int(self.server["id"])).get_channel(self.server["exchange-channel"])
			channel2 = self.bot.get_guild(int(self.server["id"])).get_channel(self.server["exchange-log-channel"])
			await channel.send(banner)
			await channel2.send(
f"""
banner: 
```
{banner}
```
member count:
```
{member_count}
```
author:
{ctx.user.mention}
|| <@&{self.server["exchanger-role"]}> ||
"""
				)
			await ctx.response.send_message("اکسچنج با موفقیت انجام شد✅\n لطفا بنر مارو تو سرورتون بزارید <#{0}>".format(self.server["banner"]), ephemeral=self.private)
		else:
			await ctx.response.send_message("تعداد ممبر ها برای اکسچنج با این سرور کم است(حداقل {0} ممبر)".format(self.server["member-limit"]), ephemeral=self.private)

class exchange(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.time = []
		self.ban = [1113088474950668399]
		self.unlimited = []
	
	@slash_command(name="exchange", description="اکسچنج")
	async def test(self, ctx:Interaction, server_name:str=nextcord.SlashOption(name="server-name", choices={x[0] : x[0] for x in cursor.execute("select name from exchange").fetchall()}),private:bool=True):
		if server_name != None:
			server = server_name
		else:
			await ctx.response.send_message("لطفا یکی از ورودی ها رو وارد کنید", ephemeral=private)
			return
		"""
		exchange_channel,
exchange_log_channel,
exchange_admin_role,
member_limit,
name,
mention_limit,
banner,
time,
guild_id,
mention,
num_id
"""
		if type(server) == str:
			y = cursor.execute(f"""select * from exchange where name="{server}" """).fetchall()[0]
			x = {
				"exchange-channel": y[0],
				"exchange-log-channel": y[1],
				"exchanger-role": y[2],
				"member-limit": y[3],
				"name": y[4],
				"mention-limit": y[5],
				"banner": y[6],
				"time": y[7],
				"id": y[8],
				"mention": y[9]
			}
		else:
			try:
				y = cursor.execute(f"select * from exchange where num_id={server}").fetchall()[0]
				x = {
					"exchange-channel": y[0],
					"exchange-log-channel": y[1],
					"exchanger-role": y[2],
					"member-limit": y[3],
					"name": y[4],
					"mention-limit": y[5],
					"banner": y[6],
					"time": y[7],
					"id": y[8],
					"mention": y[9]
				}
			except:
				await ctx.response.send_message("عدد سرور اشتباه است", ephemeral=private)
				return
		if {"user": ctx.user.id, "guild": x["id"]} in self.time and not ctx.user.id in self.unlimited:
			await ctx.response.send_message("اکسچنج در این سرور دارای {0}دقیقه cooldown است".format(x["time"]), ephemeral=private)
			return 
		if ctx.user.id in self.ban:
			await ctx.response.send_message("شما از استفاده از این کامند محروم شده اید", ephemeral=private)
			return 
		await ctx.response.send_modal(exchange2(x, self.bot, private=private))
		self.time += [{"user": ctx.user.id, "guild": x["id"]}]
		await asyncio.sleep(x["time"] * 60)
		y = 0
		for z in self.time:
			if z == {"user": ctx.user.id, "guild": x["id"]}:
				self.time[y] = {"user": 0, "guild": 0}
			y += 1

def setup(bot):
	bot.add_cog(exchange(bot))
