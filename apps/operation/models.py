# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.db import models


from apps.users.models import UserProfile
from apps.courses.models import Course


# Create your models here.


class UserAsk(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"user' name")
    mobile = models.CharField(max_length=10, verbose_name=u"cellphone number")
    course_name = models.CharField(max_length=100, verbose_name=u"name of course")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"time of ask added")

    class Meta:
        verbose_name = u"user's ask"
        verbose_name_plural = verbose_name


class CourseComments(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u'user')
    course = models.ForeignKey(Course, verbose_name=u"course")
    comments = models.CharField(max_length=200, verbose_name=u"comments")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"time of comments added")

    class Meta:
        verbose_name = u"course comments"
        verbose_name_plural = verbose_name


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"user")
    fav_id = models.IntegerField(default=0, verbose_name=u"data ID")
    fav_type = models.IntegerField(choices=((1, u"course"), (2, u"organization"), (3, u"teacher")),
                                   default=1, verbose_name=u"like type")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"time of fav added")

    class Meta:
        verbose_name = u"user favorite"
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    user_id = models.IntegerField(default=0, verbose_name=u"user who receive message") # 0 means all users
    message = models.CharField(max_length=10, verbose_name=u"message")
    has_read = models.BooleanField(default=False, verbose_name=u"whether user read the message")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"time of added")

    class Meta:
        verbose_name = u"user message"
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"user")
    course = models.ForeignKey(Course, verbose_name=u"course")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"time of comments added")

    class Meta:
        verbose_name = u"user course"
        verbose_name_plural = verbose_name
