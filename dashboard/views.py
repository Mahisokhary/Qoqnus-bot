import sqlite3

from django.http import HttpRequest, HttpResponse, JsonResponse, FileResponse
from django.shortcuts import render, redirect

def home(request: HttpRequest):
	try:
		qoqnus_id = request.COOKIES["qoqid"]
		password= request.COOKIES["password"]
		connection = sqlite3.connect('data.sqlite')
		cursor = connection.cursor()
		data = cursor.execute(f"""
		select qoqid, disid, qoq_coin, name
		from qoqnus_acc
		where qoqid="{qoqnus_id}" and password="{password}"
		""").fetchall()[0]
		html = render(request, "dashboard.html", {
			"name": data[3]
		})
		return html
		
	except Exception as e:
		#return HttpResponse(e)
		html = redirect("/acc/login")
		html.set_cookie("eror", "First login to your account")
		return html
