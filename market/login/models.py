from django.core.validators import RegexValidator
from django.db import models


class Users(models.Model):   #用户信息模型
    phone = models.CharField(max_length=20, unique=True)
    pwd = models.CharField(max_length=32)

    class Meta:
        db_table = "users"