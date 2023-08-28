from django.http import HttpRequest, HttpResponse, JsonResponse, FileResponse
from django.shortcuts import render, redirect

def index(request:HttpRequest):
	return render(request, "home.html")