# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-10-08 15:35
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name of city')),
                ('desc', models.CharField(max_length=50, verbose_name='description of city')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='time of city added')),
            ],
            options={
                'verbose_name': 'city of organization',
                'verbose_name_plural': 'city of organization',
            },
        ),
        migrations.CreateModel(
            name='Organizition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name of organization')),
                ('desc', models.TextField(verbose_name='description of the organization')),
                ('click_nums', models.IntegerField(default=0, verbose_name='number of clicks')),
                ('like_nums', models.IntegerField(default=0, verbose_name='number of likes')),
                ('address', models.CharField(max_length=100, verbose_name='address of the organizations')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.City', verbose_name='city')),
            ],
            options={
                'verbose_name': 'organization',
                'verbose_name_plural': 'organization',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name of teacher')),
                ('work_year', models.IntegerField(default=0, verbose_name='years of work experience')),
                ('work_company', models.CharField(max_length=100, verbose_name='company the teacher works for')),
                ('work_position', models.CharField(max_length=100, verbose_name='position the teacher works on')),
                ('points', models.CharField(max_length=100, verbose_name='the speciality of the teacher')),
                ('click_nums', models.IntegerField(default=0, verbose_name='number of clicks for the teacher')),
                ('like_nums', models.IntegerField(default=0, verbose_name='number of likes for the teacher')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='time of teacher added')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.Organizition', verbose_name='org name')),
            ],
            options={
                'verbose_name': 'teacher',
                'verbose_name_plural': 'teacher',
            },
        ),
    ]
