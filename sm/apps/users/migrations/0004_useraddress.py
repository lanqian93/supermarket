# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-27 17:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20181123_1636'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, verbose_name='收货人姓名')),
                ('phone', models.CharField(max_length=11, verbose_name='收货人手机号')),
                ('province', models.CharField(max_length=100, verbose_name='省')),
                ('city', models.CharField(blank=True, default='', max_length=100, verbose_name='市')),
                ('area', models.CharField(blank=True, default='', max_length=100, verbose_name='区')),
                ('street', models.CharField(max_length=255, verbose_name='街道')),
                ('isDeafault', models.BooleanField(default=False, verbose_name='是否设置默认地址')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('isDelete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Users', verbose_name='创建人')),
            ],
            options={
                'verbose_name': '收货地址管理',
                'verbose_name_plural': '收货地址管理',
            },
        ),
    ]
