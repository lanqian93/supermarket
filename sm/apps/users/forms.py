import hashlib

from django import forms
from django.core import validators
from django.core.validators import RegexValidator

#注册验证
from django_redis import get_redis_connection

from users.models import Users


class UsersForm(forms.Form):
    mobile = forms.CharField(max_length=11, required=True,
                             error_messages={"required": "手机号必填"},
                             validators=[RegexValidator(r'^1[13456789]\d{9}$', "手机号码格式错误"), ],
                             strip=True,
                             )
    password = forms.CharField(max_length=20, required=True,
                               error_messages={"required": "密码必填", "max_length": "最大长度不能超过20"})

    rpassword = forms.CharField(max_length=20, required=True,
                               error_messages={"required": "密码必填", "max_length": "最大长度不能超过20"})
    code = forms.CharField(error_messages={"required": "验证码必填!"})

    def clean(self):  #综合校验
        #得到数据
        data = self.cleaned_data
        #密码和确认密码
        if data.get("password") != data.get("rpassword"):
            #验证失败
            raise forms.ValidationError({"rpassword": "两次密码不一致"})
        else:
            #验证成功
            return data

#单个字段校验
    def clean_mobile(self):
        data = self.cleaned_data
        mobile = data.get("mobile")
        if Users.objects.filter(phone=mobile):
            raise forms.ValidationError("手机号已存在")
        else:
            return mobile
#验证码校验
    def clean_code(self):
        #获取用户表单提交的验证码
        phone = self.cleaned_data.get("mobile")
        f_code = self.cleaned_data.get("code")
        #获取redis上的验证码
        r = get_redis_connection("default")
        if phone and r.get(phone):
            s_code = r.get(phone).decode("utf-8")
            if s_code is None:
                raise forms.ValidationError("验证码不存在或者已过期")
            if f_code != s_code:
                raise forms.ValidationError("验证码错误")
            return f_code
        else:
            raise forms.ValidationError("验证码错误")


#登录验证
class LoginForm(forms.Form):
    mobile = forms.CharField(max_length=11, required=True,
                             error_messages={"required": "手机号必填", "max_length": "最大长度不能超过11"},
                             validators=[RegexValidator(r'^1[13456789]\d{9}$', "手机号码格式错误"), ],
                             strip=True,
                             )
    password = forms.CharField(max_length=20, required=True,
                               error_messages={"required": "密码必填", "max_length": "最大长度不能超过20"})

    def clean(self):  # 综合校验
        cleaned_data = self.cleaned_data
        # 获取用手机和密码
        phone = cleaned_data.get('mobile')
        password = cleaned_data.get('password')
        # 验证手机号码是否存在
        if all([phone, password]):
            # 根据手机号码获取用户
            try:
                user = Users.objects.get(phone=phone)
            except Users.DoesNotExist:
                raise forms.ValidationError({"mobile": "该用户不存在!"})

            # 判断密码是否正确
            h = hashlib.md5(password.encode("utf-8"))
            if user.password != h.hexdigest():
                raise forms.ValidationError({"password": "密码填写错误!"})

            # 正确
            # 将用户信息保存到cleaned_data中
            cleaned_data['user'] = user
            return cleaned_data
        else:
            return cleaned_data


#忘记密码校验
class ForgetForm(forms.Form):
    mobile = forms.CharField(max_length=11, required=True,
                             error_messages={"required": "手机号必填"},
                             validators=[RegexValidator(r'^1[3-9]\d{9}$', "手机号码格式错误"), ],
                             strip=True,
                             )
    password = forms.CharField(max_length=20, required=True,
                               error_messages={"required": "密码必填", "max_length": "最大长度不能超过20"})

    rpassword = forms.CharField(max_length=20, required=True,
                               error_messages={"required": "密码必填", "max_length": "最大长度不能超过20"})
    code = forms.CharField(error_messages={"required": "验证码必填!"})

    def clean(self):  #综合校验
        #得到数据
        data = self.cleaned_data
        #密码和确认密码
        if data.get("password") != data.get("rpassword"):
            #验证失败
            raise forms.ValidationError({"rpassword": "两次密码不一致"})
        else:
            #验证成功
            return data

#单个字段校验
    def clean_mobile(self):
        data = self.cleaned_data
        mobile = data.get("mobile")
        re = Users.objects.filter(phone=mobile)
        if len(re) == 0:
            raise forms.ValidationError("手机号不存在")
        else:
            return mobile
#验证码校验
    def clean_code(self):
        #获取用户表单提交的验证码
        phone = self.cleaned_data.get("mobile")
        f_code = self.cleaned_data.get("code")
        #获取redis上的验证码
        r = get_redis_connection("default")
        if phone and r.get(phone):
            s_code = r.get(phone).decode("utf-8")
            if s_code is None:
                raise forms.ValidationError("验证码不存在或者已过期")
            if f_code != s_code:
                raise forms.ValidationError("验证码错误")
            return f_code
        else:
            raise forms.ValidationError("验证码错误")


#修改个人信息校验
class UpdateUser(forms.ModelForm):
    # def clean_phone(self):
    #     phone = self.cleaned_data.get('phone')
    #     clean = self.cleaned_data
    #     if Users.objects.filter(phone=phone):
    #         raise forms.ValidationError("手机号已被占用")
    #     else:
    #         return phone
    class Meta:
        model = Users
        fields = ['phone', 'head']

        error_messages = {
            "phone": {
                "required": "手机号码必须填写!",
                "RegexValidator": "手机格式错误"
            }
        }




#添加地址验证
class AddAddressForm(forms.Form):
    school = forms.CharField(max_length=50, required=True, error_messages={"required": "宿舍必填", "max_length": "最大长度不超过50"})
    building = forms.CharField(max_length=50, required=False, error_messages={"max_length": "最大长度不超过50"})
    num = forms.CharField(max_length=50, required=False, error_messages={"max_length": "最大长度不超过50"})
    custom = forms.CharField(max_length=20, required=True, error_messages={"required": "收货人必填", "max_length": "最大长度不超过20"})
    phone = forms.CharField(max_length=11, required=True, error_messages={"required": "手机号必填", "max_length": "最大长度不超过11位"})
