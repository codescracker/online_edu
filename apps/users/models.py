# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name=u'nick name', default='')
    birth_day = models.DateField(verbose_name='birth day', null=True, blank=True)
    gender = models.CharField(max_length=20, choices=(('male', 'man'), ('female', 'woman')), default='female')
    address = models.CharField(max_length=100, default='')
    mobile = models.CharField(max_length=10, null=True, blank= True)
    image = models.ImageField(upload_to="image/%Y/%m", default=u"image/default")

    class Meta:
        verbose_name = "user's information"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u"verification code")
    email = models.EmailField(max_length=50, verbose_name=u"email adderess")
    send_type = models.CharField(
        choices=(("register", u"register email "), ("forget", "forget email"), ("update", 'update email')),
        max_length=50,
        verbose_name=u"verification code type")
    send_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = "email verification code"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{} {}'.format(self.code, self.email)


class Banner(models.Model):
    title = models.CharField(max_length= 100, verbose_name=u"title of image")
    image = models.ImageField(upload_to="banner/%Y/%m", verbose_name="banner image", max_length=100)
    url = models.CharField(max_length= 100, verbose_name= "url of the webpage")
    index = models.IntegerField(default= 1000, verbose_name= 'index of the banner image')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u"time of added")

    class Meta:
        verbose_name = u"banner images"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{} {}'.format(self.title, self.image)
