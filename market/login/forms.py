from django import forms
from django.core import validators
from django.core.validators import RegexValidator

#注册验证
from login.models import Users


class UsersForm(forms.Form):
    mobile = forms.CharField(max_length=11, required=True,
                             error_messages={"required": "手机号必填"},
                             validators=[RegexValidator(r'^1[13456789]\d{9}$', "提示信息:手机号码格式错误"), ],
                             strip=True,
                             )
    password = forms.CharField(max_length=20, required=True,
                               error_messages={"required": "密码必填", "max_length": "最大长度不能超过20"})

    rpassword = forms.CharField(max_length=20, required=True,
                               error_messages={"required": "密码必填", "max_length": "最大长度不能超过20"})

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

#登录验证
class LoginForm(forms.Form):
    mobile = forms.CharField(max_length=11, required=True,
                             error_messages={"required": "手机号必填"},
                             validators=[RegexValidator(r'^1[13456789]\d{9}$', "提示信息:手机号码格式错误"), ],
                             strip=True,
                             )
    password = forms.CharField(max_length=20, required=True,
                               error_messages={"required": "密码必填", "max_length": "最大长度不能超过20"})