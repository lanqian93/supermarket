from django.http import HttpResponse
from django.shortcuts import render, redirect
import hashlib


# Create your views here.
from login.forms import UsersForm, LoginForm
from login.models import Users

#登录
def login(request):   #登录页面
    if request.method == "POST":
        #表单验证
        form = LoginForm(request.POST)
        if form.is_valid(): #验证成功
        #接收数据
            phone = request.POST.get("mobile")
            password = request.POST.get("password")
            pwd = hashlib.md5(password.encode("utf-8"))
            #处理数据
            try:
                user = Users.objects.get(phone=phone)
            except Users.DoesNotExist:  #结果不存在错误
                return redirect("login:登录界面")
            except Users.MultipleObjectsReturned: #多个结果错误
                return redirect("login:登录界面")
            if user.pwd == pwd.hexdigest(): #判断密码
                pass   #todo
            else:
                return redirect("login:登录界面")
            #返回结果
        else:   #验证失败
            context = {
                "errors": form.errors,
                "data": form
            }
            return render(request, "login/login.html", context)
    else:
        return render(request, "login/login.html")


#注册
def zc(request):    #注册界面
    #如果请求方式是POST，表单验证
    if request.method == "POST":
        data = request.POST
        form = UsersForm(data)
        if form.is_valid():
            # 验证通过
            data = form.cleaned_data
            password = hashlib.md5(data.get("password").encode("utf-8"))
            pwd = password.hexdigest()
            Users.objects.create(phone=data.get("mobile"), pwd=pwd)
            return redirect("login:登录界面")
        else:
            #验证失败
            data = request.POST
            context = {
                "errors": form.errors,
                "data": data
            }
            return render(request, "login/reg.html", context)

    #请求方式为GET
    else:
        return render(request, 'login/reg.html')


#忘记密码
def forget(request):
    if request.method == "POST":
        pass
    else:
        return render(request, "login/forgetpassword.html")