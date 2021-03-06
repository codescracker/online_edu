# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-10-16 18:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0003_auto_20171014_0329'),
        ('courses', '0002_auto_20171013_0223'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organizations.Organizition', verbose_name='course related organization'),
        ),
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(default='courses/%Y/%m/default.jpg', upload_to='courses/%Y/%m', verbose_name='cover image'),
        ),
    ]
