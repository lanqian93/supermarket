import hashlib
import random
import re
import uuid

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django_redis import get_redis_connection

from db.base_view import BaseVerifyView
from users.forms import UsersForm, LoginForm, UpdateUser, ForgetForm, AddAddressForm, EditAddressForm
from users.helper import logining, send_sms
from users.models import Users, UserAddress

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
                # 判断链接上是否有参数next,如果有就跳转到指定的页面
                next = request.GET.get("next")
                if next:
                    return redirect(next)
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
        form = ForgetForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data.get("mobile")
            user = Users.objects.get(phone=phone)
            pwd = form.cleaned_data.get("password")
            p = hashlib.md5(pwd.encode("utf-8"))
            user.password = p.hexdigest()
            user.save()
            return redirect("user:登录")
        else:
            context = {
                "errors": form.errors
            }
            return render(request, "user/forgetpassword.html", context)



"""用户中心"""
class MemberView( BaseVerifyView):
    def get(self, request):
        context = {
            "phone": request.session.get('phone'),
            "head": request.session.get('head'),
        }
        return render(request, "user/member.html", context)
    def post(self, request):
        pass


"""用户信息"""
class UserInforView(BaseVerifyView):
    def get(self, request):
        id = request.session['id']
        user = Users.objects.get(pk=id)
        context = {
            "user": user,
            "head": request.session.get("head")
        }
        return render(request, "user/infor.html", context)
    def post(self, request):
        #接收数据
        data = request.POST
        #处理数据
        #校验
        form = UpdateUser(data,request.FILES)
        if form.is_valid():
            id = request.session['id']
            phone = data.get("phone")
            nickname = data.get("nickname")
            gender = data.get("gender")
            school_name = data.get("school_name")
            hometown = data.get("hometown")
            birth_of_date = data.get("birth_of_date")
            address = data.get("address")
            user = Users.objects.get(pk=id)
            user.phone = phone
            user.nickname = nickname
            user.school_name = school_name
            user.hometown = hometown
            user.birth_of_date = birth_of_date
            user.address = address
            user.gender = gender

            cleaned_data = form.cleaned_data

            if request.FILES.get('head'):
                user.head = cleaned_data.get('head')
            user.save()
            #重写session
            logining(request, user)
            context = {
                "user": user
            }
            return redirect("user:用户中心")
        else:
            id = request.session['id']
            user = Users.objects.get(pk=id)
            context = {
                "errors": form.errors,
                "user": user
            }
            return render(request, "user/infor.html", context)



"""收货地址列表"""
class AddressListView(BaseVerifyView):
    def get(self, request):
        #查询用户收货地址，显示到页面上，默认的显示在最上面
        address = UserAddress.objects.filter(user_id=request.session.get("id"), isDelete=False).order_by("-isDeafault")
        context = {
            "address": address
        }
        return render(request, "user/gladdress.html", context)
    def post(self, request):
        pass


"""添加收货地址"""
class AddAddressView(BaseVerifyView):
    def get(self, request):
        return render(request, "user/address.html")
    def post(self, request):
        #接受数据
        data = request.POST.dict()
        data['user'] = request.session.get("id")
        #验证数据
        form = AddAddressForm(data)
        if form.is_valid():
            clean_data = form.cleaned_data
            clean_data["user"] = Users.objects.get(pk=request.session.get("id"))
            UserAddress.objects.create(**clean_data)
            return redirect("user:收货地址列表")
        else:
            context = {
                "error": form.errors,
                "form": form
            }
            return render(request, "user/address.html", context)



"""收货地址修改"""
class AddressEditView(BaseVerifyView):
    def get(self, request, id):
        #根据id回显收货地址信息
        user_id = request.session.get("id")
        try:
            address = UserAddress.objects.get(user_id=user_id, pk=id)
        except address.DoesNotExist:
            return redirect("user:收货地址列表")
        context = {
            "address": address
        }
        return render(request, "user/address_edit.html", context)

    def post(self, request, id):
        #接收参数
        data = request.POST.dict()
        user_id = request.session.get("id")
        data['user_id'] = user_id
        address_id = data.get("id")
        form = EditAddressForm(data)
        if form.is_valid():
            #根据收货地址id更新数据
            clean_data = form.cleaned_data
            UserAddress.objects.filter(user_id=user_id, pk=address_id).update(**clean_data)
            return redirect("user:收货地址列表")
        else:
            context = {
                "error": form.errors,
                "form": form,
                "address": data,
            }
            return render(request, "user/address_edit.html", context)


"""收货地址删除"""
class AdressDelView(BaseVerifyView):
    def get(self, request):
        return JsonResponse({"code": 1, "errmsg": "请求方式错误"})
    def post(self, request):
        #获取传入的商品id，根据id删除商品信息
        #最好也要判断用户id
        user_id = request.session.get("id")
        id = request.POST.get("address_id")
        if user_id is None:
            return JsonResponse({"code": 2, "errmsg": "请登录"})
        UserAddress.objects.filter(user_id=user_id, pk=id).update(isDelete=True)
        return JsonResponse({"code": 0})


"""设置默认收货地址"""
def defaultAddress(request):
    if request.method == "POST":
        #接收传入的商品id，当前商品设置为默认，其他的不是默认
        id = request.POST.get("address_id")
        user_id = request.session.get("id")
        if user_id is None:
            return JsonResponse({"code": 1, "errmsg": "没有登录"})
        UserAddress.objects.all().update(isDeafault=False)
        UserAddress.objects.filter(user_id=user_id, pk=id).update(isDeafault=True)
        return JsonResponse({"code": 0})
    else:
        return JsonResponse({"code": 2, "errmsg": "参数错误"})
"""发送验证码"""
def send_code(request):
    if request.method == "POST":
        #接收手机号
        phone = request.POST.get("mobile", "")
        # 验证手机格式是否正确
        phone_re = re.compile("^1[3-9]\d{9}$")
        rs = re.search(phone_re, phone)
        if rs is None: #验证失败
            return JsonResponse({"err": 1, "msg": "手机格式错误"})
        # 生成随机码 随机数字组成
        r_code = "".join([str(random.randint(0, 9)) for _ in range(4)])

        #将随机码保存到redis上面
        r = get_redis_connection("default")
        r.set(phone, r_code)
        r.expire(phone, 120)

        #发送短信
        print(r_code)
        # __business_id = uuid.uuid1()
        # params = "{\"code\":\"%s\",\"product\":\"yshs\"}" % r_code
        # print(send_sms(__business_id, phone, "注册验证", "SMS_2245271", params))
        return JsonResponse({"err": 0})
    else:
        return JsonResponse({"err": 1, "msg": "请求方式错误"})

