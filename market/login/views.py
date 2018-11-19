from django.http import HttpResponse
from django.shortcuts import render, redirect
import hashlib


# Create your views here.
from login.forms import UsersForm, LoginForm, AddAddressForm
from login.models import Users, Address


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
                return redirect("login:个人中心界面")
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


#个人中心
def member(request):
    return render(request, "login/member.html")


#收货地址
def address(request):
    #添加数据
    user = Users.objects.get(pk=4)
    # user.address_set.create(address="长安路长安街")
    # user.address_set.create(address="天信路22号")

    #回显
    addresses = user.address_set.all()
    context = {
       "user": user,
        "addresses": addresses
    }
    return render(request, 'login/gladdress.html', context)


#添加地址
def addAddress(request):
    if request.method == "POST":
        addresses = Address.objects.all()
        if len(addresses) < 6:   #地址小于6个
            #表单验证
            form = AddAddressForm(request.POST)
            #验证成功
            if form.is_valid():
            # 接收数据
            # 处理数据
                school = request.POST.get("school")
                building = request.POST.get("building")
                num = request.POST.get("num")
                custom = request.POST.get("custom")
                phone = request.POST.get("phone")
                address = school + building + num
                user_id=4
                Address.objects.create(address=address, custom_name=custom, phone=phone, user_id=user_id)
            #返回数据
                return redirect("login:收货地址界面")
            #验证失败
            else:
                context = {
                    "errors": form.errors,
                }
                return render(request, "login/address.html", context)
        else:
            return render(request, "login/address.html")
    return render(request, "login/address.html")


#定位
def location(request):
    return render(request, "login/location.html")