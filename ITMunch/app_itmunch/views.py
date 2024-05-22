from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'app_itmunch/index.html')

def login_view(request):
    return HttpResponse("Hello World!")

def register_view(request):
    return HttpResponse("Hello World!")

def logout_view(request):
    return HttpResponse("Hello World!")