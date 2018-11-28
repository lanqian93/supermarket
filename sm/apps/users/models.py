from django.core.validators import RegexValidator
from django.db import models

class Users(models.Model):
    """
        用户表
    """
    sex_choices = (
        (1, "男"),
        (2, "女"),
    )
    phone = models.CharField(max_length=11,
                             verbose_name="手机号码",
                             validators=[
                                 RegexValidator(r'^1[3-9]\d{9}$', "手机号码格式错误!")
                             ])
    nickname = models.CharField(max_length=50, null=True, blank=True, verbose_name="昵称")
    password = models.CharField(max_length=32, verbose_name="密码")
    gender = models.SmallIntegerField(choices=sex_choices, default=1, verbose_name="性别")
    school_name = models.CharField(max_length=50, null=True, blank=True, verbose_name="学校")
    hometown = models.CharField(max_length=50, null=True, blank=True, verbose_name="家乡")
    birth_of_date = models.DateField(null=True, blank=True, verbose_name="出生日期")
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name="详细位置")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    isDelete = models.BooleanField(default=False, verbose_name="是否删除")
    head = models.ImageField(upload_to="head/%Y%m", default="head/memtx.png",blank=True, verbose_name="用户头像")
    def __str__(self):
        return self.phone

    class Meta:
        db_table = "user"
        verbose_name = "用户管理"
        verbose_name_plural = verbose_name



"""收货地址"""
class UserAddress(models.Model):
    user = models.ForeignKey(to="Users", verbose_name="创建人")
    username = models.CharField(max_length=50, verbose_name="收货人姓名")
    phone = models.CharField(max_length=11, verbose_name="收货人手机号",
                             validators=[
                                 RegexValidator(r'^1[3-9]\d{9}$', "手机号码格式错误!")
                             ])
    hcity = models.CharField(max_length=100, verbose_name="省",  blank=True, null=True)
    hproper = models.CharField(max_length=100, verbose_name="市", blank=True, null=True)
    harea = models.CharField(max_length=100, verbose_name="区",)
    street = models.CharField(max_length=255, verbose_name="街道")
    isDeafault = models.BooleanField(default=False, blank=True, verbose_name="是否设置默认地址")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    isDelete = models.BooleanField(default=False, verbose_name="是否删除")
    class Meta:
        verbose_name = "收货地址管理"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.username

