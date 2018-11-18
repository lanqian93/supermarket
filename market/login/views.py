from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def login(request):   #登录页面
    return render(request, "login/login.html")