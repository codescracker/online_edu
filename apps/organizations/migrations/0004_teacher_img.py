# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-10-16 19:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0003_auto_20171014_0329'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='img',
            field=models.ImageField(default='teachers/%Y/%m/default.jpg', upload_to='teachers/%Y/%m', verbose_name='teacher image'),
        ),
    ]
