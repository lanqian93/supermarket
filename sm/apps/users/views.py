import hashlib

from django.shortcuts import render, redirect
from django.views import View

from db.base_view import BaseVerifyView
from users.forms import UsersForm, LoginForm, UpdateUser
from users.helper import logining
from users.models import Users

"""注册视图"""
class RegistView(View):
    def get(self, request):
        return render(request, 'user/reg.html')

    def post(self, request):
        data = request.POST
        form = UsersForm(data)
        if form.is_valid():
            # 验证通过
            data = form.cleaned_data
            password = hashlib.md5(data.get("password").encode("utf-8"))
            pwd = password.hexdigest()
            Users.objects.create(phone=data.get("mobile"), password=pwd)
            return redirect("user:登录")
        else:
            # 验证失败
            data = request.POST
            context = {
                "errors": form.errors,
                "data": data
            }
            return render(request, "user/reg.html", context)


"""登录视图"""
class LoginView(View):
    def get(self, request):
        return render(request, "user/login.html")
    def post(self, request):
        # 表单验证
        form = LoginForm(request.POST)
        if form.is_valid():  # 验证成功
                #保存登录的session
                user = form.cleaned_data.get("user")
                logining(request, user)
                return redirect("user:用户中心")
            # 返回结果
        else:  # 验证失败
            context = {
                "errors": form.errors,
                "data": form
            }
            return render(request, "user/login.html", context)


"""忘记密码"""
class ForgetView(View):
    def get(self, request):
        return render(request, "user/forgetpassword.html")
    def post(self, request):
        pass

"""用户中心"""
class MemberView( BaseVerifyView):
    def get(self, request):
        return render(request, "user/member.html")
    def post(self, request):
        pass


"""用户信息"""
class UserInforView(BaseVerifyView):
    def get(self, request):
        id = request.session['id']
        user = Users.objects.get(pk=id)
        context = {
            "user": user
        }
        return render(request, "user/infor.html", context)
    def post(self, request):
        #接收数据
        data = request.POST
        #处理数据
        #校验
        form = UpdateUser(data)
        if form.is_valid():
            id = request.session['id']
            phone = data.get("phone")
            nickname = data.get("nickname")
            gender = data.get("gender")
            school_name = data.get("school_name")
            hometown = data.get("hometown")
            birth_of_date = data.get("birth_of_date")
            address = data.get("address")
            if birth_of_date:
                user = Users.objects.filter(pk=id).update(phone=phone, nickname=nickname, gender=gender,
                                                   school_name=school_name, hometown=hometown,
                                                   birth_of_date=birth_of_date, address=address)
                user = Users.objects.get(pk=id)
                context = {
                    "user": user
                }
                return render(request, "user/infor.html", context)
            else:
                Users.objects.filter(pk=id).update(phone=phone, nickname=nickname, gender=gender,
                                                   school_name=school_name,
                                                   hometown=hometown, address=address
                                                   )
                user = Users.objects.get(pk=id)
                context = {
                    "user": user
                }
                return render(request, "user/infor.html", context)
        else:
            id = request.session['id']
            user = Users.objects.get(pk=id)
            context = {
                "errors": form.errors,
                "user": user
            }
            return render(request, "user/infor.html", context)
