from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.utils import timezone

def home(request):
 return render(request,"index.html")
# def index(request):
    
#  return render(request,"index.html")

