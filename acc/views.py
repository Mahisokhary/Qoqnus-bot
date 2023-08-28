import sqlite3

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

def login(request:HttpRequest):
	try:
		if request.method == "POST":
			qoqnus_id = request.POST["qoqnus_id"]
			password = request.POST["password"]
			for i in [qoqnus_id, password]:
				if "\"" in i or "'" in i:
					html = redirect("/acc/login")
					html.set_cookie("eror", "input should not contain ' and \" ")
					return html
			connection = sqlite3.connect("data.sqlite")
			cursor = connection.cursor()
			data = cursor.execute(f"select * from qoqnus_acc where qoqid='{qoqnus_id}' and password='{password}' ").fetchall()
			if len(data) == 0:
				html = redirect("/acc/login")
				html.set_cookie("eror", "Username or Password is incorrect")
				return html
			else:
				html = redirect("/dashboard/")
				html.set_cookie("qoqid", qoqnus_id)
				html.set_cookie("password", password)
				return html
		else:
			try:
				eror = request.COOKIES["eror"]
			except:
				eror = ""
			html = render(request, "reg.html", {"eror": eror})
			html.delete_cookie("eror")
			return html
	except Exception as e:
		return #HttpResponse(e)

def logout(request:HttpRequest):
	html = redirect("/acc/login")
	html.set_cookie("eror", "Log out was successful")
	html.delete_cookie("qoqid")
	html.delete_cookie("password")
	return html
