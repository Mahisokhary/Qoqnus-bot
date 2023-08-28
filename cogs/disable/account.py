import nextcord
import sqlite3
import asyncio

from nextcord.ext import commands
from nextcord import Interaction
from nextcord import slash_command
from typing import Literal

connection = sqlite3.connect('data.sqlite')
cursor = connection.cursor()


cursor.execute("""
    CREATE TABLE IF NOT EXISTS qoqnus_acc (
        disid INTEGER,
        qoqid varchar(255),
        qoq_coin INTEGER DEFAULT 0,
        telid varchar(255) DEFAULT None,
        email varchar(255) DEFAULT None,
        mobile varchar(255),
        name varchar(255),
        password varchar(255)
    )
""")
connection.commit()

class account(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.blocked = []
	
	@slash_command(name = "see-account", description = "مشاهده اکانت ققنوس مستر")
	async def see_account(self, ctx:Interaction):
		x = cursor.execute(f"select * from qoqnus_acc where disid={ctx.user.id}").fetchone()
		if x != None:
			embed = nextcord.Embed(color=nextcord.Colour.green())
			
			#(1019484919195521034, 'qoqnus_master', 0, 'qoqnus_master', 'None', 'None', 'Qoqnus master', '178558mahanmn')
			embed.add_field(inline=False,name="اطلاعات اکانت شما:", value="")
			embed.add_field(inline=False,name="", value="نام: {0} 📌".format(x[6]))
			embed.add_field(inline=False,name="", value="آیدی ققنوس: {0} 👤".format(x[1]))
			embed.add_field(inline=False,name="", value="آیدی دیسکورد: {0} 👤".format(x[0]))
			embed.add_field(inline=False,name="", value="نام کاربری تلگرام: {0} 👤".format(x[3]))
			embed.add_field(inline=False,name="", value="قوق کوین: {0} 💳".format(x[2]))
			embed.add_field(inline=False,name="", value="شماره موبایل: {0} 📱".format(x[5]))
			embed.add_field(inline=False,name="", value="ایمیل: {0} ✉️".format(x[4]))
			
			await ctx.response.send_message(embed=embed, ephemeral=True)
		else:
			await ctx.response.send_message("شما اکانت ندارید ابتدا یک اکانت بسازید", ephemeral=True)
	
	@slash_command(name="create-account", description="ساخت اکانت ققنوس مستر")
	async def create_account(self, ctx:Interaction, qoqnus_id:str, password:str, name:str="None",mobile:str="None", email:str="None"):
		qoqnus_id = qoqnus_id.lower()
		args = [qoqnus_id, password, name, mobile, email]
		if len(password) < 8:
			await ctx.response.send_message("رمز خیلی کوتاه است (حداقل ۸ رقم)", ephemeral=True)
			return
		if len(cursor.execute(f"select * from qoqnus_acc where qoqid='{qoqnus_id}'").fetchall()) != 0:
			await ctx.response.send_message("این نام کاربری استفاده شده است", ephemeral=True)
			return 
		valid_id = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "_"]
		for letter in qoqnus_id:
			if not letter in valid_id:
				await ctx.response.send_message("نام کاربری باید شامل اعداد و حروف اینگلیسی و _ باشد", ephemeral=True)
				return 
		if name == "None":
			if "\"" in ctx.user.name and "'" in ctx.user.name:
				name = "None"
			else:
				name = ctx.user.name
		if len(cursor.execute(f"select * from qoqnus_acc where disid={ctx.user.id}").fetchall()) == 0:
			for i in args:
				if "\"" in i or "'" in i:
					await ctx.response.send_message("هیچ کدام از ورودی ها نباید شامل \" یا ' باشد", ephemeral=True)
					return
			cursor.execute("""
				insert into qoqnus_acc values
				({0},"{1}", 0, "None", "{2}", "{3}", "{4}","{5}")
			""".format(ctx.user.id, qoqnus_id, email, mobile, name, password))
			connection.commit()
			await ctx.response.send_message("اکانت شما با موفقیت ساخته شد", ephemeral=True)
		else:
			await ctx.response.send_message("شما قبلا اکانت ققنوس مستر ساخته اید", ephemeral=True)
	
	@slash_command(name="send_qoqcoin", description="ارسال قوق کوین به دیگران")
	async def send_money(self, ctx:Interaction, receiver:nextcord.Member, value:int, reason:str=None, private:bool=False):
		if len(cursor.execute(f"select * from qoqnus_acc where disid={receiver.id}").fetchall()) == 0:
			await ctx.response.send_message("کاربر انتخاب شده اکانت ققنوس مستر ندارد")
			return
		if len(cursor.execute(f"select * from qoqnus_acc where disid={ctx.user.id}").fetchall()) == 0:
			await ctx.response.send_message("شما اکانت ققنوس مستر ندارید")
			return
		if value < 0:
			await ctx.response.send_message("ارسال مقدار منفی مقدور نیست", ephemeral=private)
		receiver_balance = cursor.execute(f"select * from qoqnus_acc where disid={receiver.id}").fetchone()[2]
		sender_balance = cursor.execute(f"select * from qoqnus_acc where disid={ctx.user.id}").fetchone()[2]
		if sender_balance < value:
			await ctx.response.send_message("موجودی شما کافی نمیباشد")
			return 
		cursor.execute("""
			UPDATE qoqnus_acc
			SET qoq_coin = {0}
			WHERE disid={1};
		""".format(sender_balance - value, ctx.user.id))
		connection.commit()
		cursor.execute("""
			update qoqnus_acc
			set qoq_coin = {0}
			where disid={1};
		""".format(receiver_balance + value, receiver.id))
		connection.commit()
		embed = nextcord.Embed(color=nextcord.Colour.green())
		embed.add_field(inline=False,name="تراکنش با موفقیت انجام شد", value="مقدار: {0} 💸".format(value))
		embed.add_field(inline=False,name="", value="ارسال کننده: {0} 💳".format(ctx.user.mention))
		embed.add_field(inline=False,name="", value="دریافت کننده: {0} 💳".format(receiver.mention))
		if reason != None: embed.add_field(name="دلیل:", value=reason)
		
		await self.bot.get_channel(1129020728184938627).send(embed=embed)
		await ctx.response.send_message(embed=embed, ephemeral=private)
		await receiver.send(embed=embed)
	@slash_command(name="delete-account", description="حذف اکانت ققنوس مستر")
	async def delete_account(self, ctx:Interaction, realy:bool, really2:bool, reallyyyyy:bool):
		if realy and really2 and reallyyyyy:
			if len(cursor.execute(f"select * from qoqnus_acc where disid={ctx.user.id}").fetchall()) == 0:
				await ctx.response.send_message("شما اکانت ققنوس مستر ندارید")
			else:
				cursor.execute("""
					DELETE FROM qoqnus_acc
					WHERE disid = {0};
				""".format(ctx.user.id))
				connection.commit()
				await ctx.response.send_message("اکانت شما با موفقیت حذف شد \n خداحافظ رفیق😭💔", ephemeral=True)
	@slash_command(name="see-others-account", description="حساب کاربری بقیه رو نگاه کن")
	async def see_other_account(self, ctx:Interaction, user:nextcord.Member):
		x = cursor.execute(f"select * from qoqnus_acc where disid={user.id}").fetchall()
		if len(x) == 0:
			await ctx.response.send_message("این کاربر اکانت ققنوس مستر ندارد")
		else:
			embed = nextcord.Embed(color=nextcord.Colour.green())
			x = x[0]
			#(1019484919195521034, 'qoqnus_master', 0, 'qoqnus_master', 'None', 'None', 'Qoqnus master', '178558mahanmn')
			embed.add_field(inline=False,name="اطلاعات اکانت {0}:".format(user.mention), value="")
			embed.add_field(inline=False,name="", value="نام: {0} 📌".format(x[6]))
			embed.add_field(inline=False,name="", value="آیدی ققنوس: {0} 👤".format(x[1]))
			embed.add_field(inline=False,name="", value="آیدی دیسکورد: {0} 👤".format(x[0]))
			embed.add_field(inline=False,name="", value="نام کاربری تلگرام: {0} 👤".format(x[3]))
			embed.add_field(inline=False,name="", value="قوق کوین: {0} 💳".format(x[2]))
			await ctx.response.send_message(embed=embed)
	@slash_command(name="change-account-details", description="برای راهنما هیچ ورودی وارد نکن")
	async def change_account_details(self, ctx:Interaction, type:Literal["password", "qoqnus id", "mobile number", "name", "value"]=None, value:str=None, value2:str=None):
		if type == None and value == None:
			
			embed = nextcord.Embed(color=nextcord.Colour.green())
			embed.set_thumbnail(url=self.bot.application.icon.url)
			
			embed.add_field(inline=False, name="تغییر رمز:", value="type=password\nvalue=رمز جدید\nvalue2=تکرار رمز جدید")
			embed.add_field(inline=False, name="تغییر نام کاربری:", value="type=qoqnus id\nvalue=نام کاربری جدید")
			embed.add_field(inline=False, name="تغییر شماره موبایل:", value="type=mobile number\nvalue=شماره موبایل جدید")
			embed.add_field(inline=False, name="تغییر ایمیل", value="type=email\nvalue=ایمیل جدید")
			embed.add_field(inline=False, name="تغییر نام", value="type=name\nvalue=نام جدید")
			
			await ctx.response.send_message("راهنما:", embed=embed)
			
		args = [type, value]
		x, y = None, None
		for i in args:
			if "\"" in i or "'" in args:
				await ctx.response.send_message("ورودی ها نباید شامل \" یا ' باشد", ephemeral=True)
				return
		if type == "password":
			if len(value) < 8:
				await ctx.response.send_message("رمز خیلی کوتاه است (حداقل ۸ رقم)", ephemeral=True)
				return
			if not value == value2:
				await ctx.response.send_message("رمز وارد شده با تکرار آن مساوی نیست", ephemeral=True)
				return 
			x = "password"
			y = value
		elif type == "qoqnus id":
			await ctx.response.send_message("هم اکنون تغییر ققنوس آیدی امکان پذیر نیست برای راهنمایی بیشتر به ادمین اطلاع بدید", ephemeral=True)
			return 
			if len(cursor.execute(f"select * from qoqnus_acc where qoqid='{value}'").fetchall()) != 0:
				await ctx.response.send_message("این نام کاربری استفاده شده است", ephemeral=True)
				return
			valid_id = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "_"]
			for letter in value:
				if not letter in valid_id:
					await ctx.response.send_message("نام کاربری باید شامل اعداد و حروف اینگلیسی و _ باشد", ephemeral=True)
					return
			x = "qoqid"
			y = value
		elif type == "phone number":
			x = "mobile"
			y = value
		elif type == "email":
			x = "email"
			y = value
		elif type == "name":
			x = "name"
			y = value
		else:
			await ctx.response.send_message("نوع وارد شده اشتباه است", ephemeral=True)
			return 
		cursor.execute(f"""
			update qoqnus_acc
			set {x}="{y}"
			where disid="{ctx.user.id}"
		""")
		await ctx.response.send_message("درخواست شما با موفقیت انجام شد✅", ephemeral=True)
	@slash_command(name="login", description="اکانت ققنوست رو از یه اکانت دیسکورد دیگه به این اکانتت انتقال بده")
	async def login(self, ctx:Interaction, qoqnus_id:str, password:str):
		args = [qoqnus_id, password]
		for i in args:
			if "\"" in i or "'" in args:
				await ctx.response.send_message("ورودی ها نباید شامل \" یا ' باشد به دلایل امنیتی ۲دقیقه دیگر دوباره تلاش کنید", ephemeral=True)
				n = nextcord.Embed(color=nextcord.Colour.red())
				n.add_field(inline=False, name="تلاش برای sql injection", value="تلاش نا موفق {0} برای ورود به حساب {1}".format(ctx.user.mention, qoqnus_id))
				await self.bot.get_channel(1129021722667012157).send(embed=n)
				self.blocked += [ctx.user.id]
				await asyncio.sleep(120)
				x = 0
				for i in self.blocked:
					if i == ctx.user.id:
						self.blocked[x] = 0
						return
					x += 1
				return
		if ctx.user.id in self.blocked:
			await ctx.response.send_message("شما مسدود شده اید", ephemeral=True)
			return 
		if len(cursor.execute(f"""select * from qoqnus_acc where disid={ctx.user.id}""").fetchall()) != 0:
			await ctx.response.send_message("شما هم اکنون اکانت دارید برای اتصال یک اکانت دیگر به این حساب دیسکورد ابتدا اکانت فعلی را حذف کنید", ephemeral=True)
			return 
		if len(cursor.execute(f"""select * from qoqnus_acc where qoqid="{qoqnus_id}" and password="{password}" """).fetchall()) == 0:
			n = nextcord.Embed(color=nextcord.Colour.red())
			n.add_field(inline=False, name="", value="ورود به سیستم ناموفق از حساب {0}\nبه حساب {1}".format(ctx.user.mention, qoqnus_id))
			await self.bot.get_channel(1129021722667012157).send(embed=n)
			await ctx.response.send_message("اطلاعات وارد شده غلط میباشد 2دقیقه دیگر مجددا تلاش کنید" , ephemeral=True)
			self.blocked += [ctx.user.id]
			await asyncio.sleep(120)
			x = 0
			for i in self.blocked:
				if i == ctx.user.id:
					self.blocked[x] = 0
					return
				x += 1
		cursor.execute("""
			UPDATE qoqnus_acc
			SET disid = {0}
			WHERE qoqid="{1}" and password="{2}";
		""".format(ctx.user.id, qoqnus_id, password))
		connection.commit()
		n = nextcord.Embed(color=nextcord.Colour.green())
		n.add_field(inline=False, name="", value="ورود به سیستم از حساب {0}\nبه حساب {1}".format(ctx.user.mention, qoqnus_id))
		await self.bot.get_channel(1129021722667012157).send(embed=n)
		await ctx.response.send_message("شما با موفقیت وارد سیستم شدید", ephemeral=True)

def setup(bot):
	bot.add_cog(account(bot))
