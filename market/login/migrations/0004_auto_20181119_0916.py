# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-19 01:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_auto_20181119_0915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='phone',
            field=models.CharField(max_length=20),
        ),
    ]
