from django import forms
from django.core import validators
from django.core.validators import RegexValidator

#注册验证
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

#登录验证
class LoginForm(forms.Form):
    mobile = forms.CharField(max_length=11, required=True,
                             error_messages={"required": "手机号必填", "max_length": "最大长度不能超过11"},
                             validators=[RegexValidator(r'^1[13456789]\d{9}$', "手机号码格式错误"), ],
                             strip=True,
                             )
    password = forms.CharField(max_length=20, required=True,
                               error_messages={"required": "密码必填", "max_length": "最大长度不能超过20"})



#修改个人信息校验
class UpdateUser(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['phone', ]

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
