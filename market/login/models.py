from django.core.validators import RegexValidator
from django.db import models



#用户信息模型
class Users(models.Model):
    phone = models.CharField(max_length=20, unique=True)
    pwd = models.CharField(max_length=32)

    class Meta:
        db_table = "users"



#用户地址模型
class Address(models.Model):
    user = models.ForeignKey(to='Users', on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    custom_name = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    isDel = models.BooleanField(default=False)