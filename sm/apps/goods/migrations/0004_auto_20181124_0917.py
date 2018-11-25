# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-24 09:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_auto_20181123_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='order',
            field=models.SmallIntegerField(default=0, verbose_name='排序'),
        ),
        migrations.AlterField(
            model_name='goodsimg',
            name='url',
            field=models.ImageField(upload_to='goods_gallery/%Y%m/%d', verbose_name='商品相册'),
        ),
    ]
