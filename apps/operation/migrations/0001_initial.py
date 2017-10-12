# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-10-08 15:35
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseComments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.CharField(max_length=200, verbose_name='comments')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='time of comments added')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course', verbose_name='course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'course comments',
                'verbose_name_plural': 'course comments',
            },
        ),
        migrations.CreateModel(
            name='UserAsk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name="user' name")),
                ('mobile', models.CharField(max_length=10, verbose_name='cellphone number')),
                ('course_name', models.CharField(max_length=100, verbose_name='name of course')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='time of ask added')),
            ],
            options={
                'verbose_name': "user's ask",
                'verbose_name_plural': "user's ask",
            },
        ),
        migrations.CreateModel(
            name='UserCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='time of comments added')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course', verbose_name='course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'user course',
                'verbose_name_plural': 'user course',
            },
        ),
        migrations.CreateModel(
            name='UserFavorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fav_id', models.IntegerField(default=0, verbose_name='data ID')),
                ('fav_type', models.IntegerField(choices=[(1, 'course'), (2, 'organization'), (3, 'teacher')], default=1, verbose_name='like type')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='time of fav added')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'user favorite',
                'verbose_name_plural': 'user favorite',
            },
        ),
        migrations.CreateModel(
            name='UserMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(default=0, verbose_name='user who receive message')),
                ('message', models.CharField(max_length=10, verbose_name='message')),
                ('has_read', models.BooleanField(default=False, verbose_name='whether user read the message')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='time of added')),
            ],
            options={
                'verbose_name': 'user message',
                'verbose_name_plural': 'user message',
            },
        ),
    ]
