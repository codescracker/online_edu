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
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name of the course')),
                ('desc', models.CharField(max_length=200, verbose_name='description of the course')),
                ('detail', models.TextField(verbose_name='detail of the course')),
                ('degree', models.CharField(choices=[('Easy', 'easy level course'), ('Medium', 'medium level course'), ('Hard', 'hard level of course')], max_length=20, verbose_name='difficulty level of degree')),
                ('learn_time', models.IntegerField(default=0, verbose_name='length of the course')),
                ('students', models.IntegerField(default=0, verbose_name='number of student')),
                ('like_nums', models.IntegerField(default=0, verbose_name='number of likes')),
                ('image', models.ImageField(upload_to='courses/%Y/%m', verbose_name='cover image')),
                ('click_nums', models.IntegerField(default=0, verbose_name='number of click')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='time of creation of course')),
            ],
            options={
                'verbose_name': 'courses',
                'verbose_name_plural': 'courses',
            },
        ),
        migrations.CreateModel(
            name='CourseRsource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='source name')),
                ('download', models.FileField(upload_to='course/resource/%Y/%m')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='time of source added')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.courses.Course', verbose_name='course')),
            ],
            options={
                'verbose_name': 'course resource',
                'verbose_name_plural': 'course resource',
            },
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='lecture name')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='time of lecture added')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.courses.Course', verbose_name='course')),
            ],
            options={
                'verbose_name': 'lecutre',
                'verbose_name_plural': 'lecutre',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='video name')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='time of video added')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.courses.Lecture', verbose_name='lesson')),
            ],
            options={
                'verbose_name': 'video',
                'verbose_name_plural': 'video',
            },
        ),
    ]