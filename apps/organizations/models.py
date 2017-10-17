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

    def __unicode__(self):
        return self.name


class Organizition(models.Model):
    city = models.ForeignKey(City, verbose_name=u"city")
    name = models.CharField(max_length=50, verbose_name=u"name of organization")
    desc = models.TextField(verbose_name=u'description of the organization')
    click_nums = models.IntegerField(default=0, verbose_name=u"number of clicks")
    like_nums = models.IntegerField(default=0, verbose_name=u"number of likes")
    address = models.CharField(max_length=100, verbose_name=u"address of the organizations")
    img = models.ImageField(upload_to="organizations/%Y/%m", verbose_name=u"organization image", max_length=100,
                            default='organizations/%Y/%m/default.jpg')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='time of organization added')
    category = models.CharField(max_length=50,
                                choices=(('Education Organization', 'training org'),
                                                        ('Individual', 'person'),
                                                        ('College', 'higher education')),
                                verbose_name='Org type',
                                default='Individual')
    student_num = models.IntegerField(default=0, verbose_name=u"number of students")
    course_num = models.IntegerField(default=0, verbose_name=u"number of courses")

    class Meta:
        verbose_name = u"organization"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return "{} {}".format(self.city, self.name)


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
    img = models.ImageField(upload_to="teachers/%Y/%m", verbose_name=u"teacher image", max_length=100,
                            default='teachers/%Y/%m/default.jpg')

    class Meta:
        verbose_name = u"teacher"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return "{} {}".format(self.organization, self.name)
