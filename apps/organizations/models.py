# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.db import models

# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"name of city")
    desc = models.CharField(max_length=50, verbose_name=u"description of city")
    add_time = models.DateTimeField(default=datetime.now, verbose_name='time of city added')

    class Meta:
        verbose_name = u"city of organization"
        verbose_name_plural = verbose_name


class Organizition(models.Model):
    city = models.ForeignKey(City, verbose_name=u"city")
    name = models.CharField(max_length=50, verbose_name=u"name of organization")
    desc = models.TextField(verbose_name=u'description of the organization')
    click_nums = models.IntegerField(default=0, verbose_name=u"number of clicks")
    like_nums = models.IntegerField(default=0, verbose_name=u"number of likes")
    address = models.CharField(max_length=100, verbose_name=u"address of the organizations")

    class Meta:
        verbose_name = u"organization"
        verbose_name_plural = verbose_name


class Teacher(models.Model):
    organization = models.ForeignKey(Organizition, verbose_name=u"org name")
    name = models.CharField(max_length=100, verbose_name=u"name of teacher")
    work_year = models.IntegerField(default=0, verbose_name=u"years of work experience")
    work_company = models.CharField(max_length=100, verbose_name=u"company the teacher works for")
    work_position = models.CharField(max_length=100, verbose_name=u"position the teacher works on")
    points = models.CharField(max_length=100, verbose_name=u"the speciality of the teacher")
    click_nums = models.IntegerField(default=0, verbose_name=u"number of clicks for the teacher")
    like_nums = models.IntegerField(default=0, verbose_name=u"number of likes for the teacher")
    add_time = models.DateTimeField(default=datetime.now, verbose_name='time of teacher added')

    class Meta:
        verbose_name = u"teacher"
        verbose_name_plural = verbose_name
