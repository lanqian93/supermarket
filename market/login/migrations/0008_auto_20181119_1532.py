# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-19 07:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0007_auto_20181119_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='custom_name',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='address',
            name='phone',
            field=models.CharField(max_length=20),
        ),
    ]
