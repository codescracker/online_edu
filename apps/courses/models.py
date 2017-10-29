# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.db import models


from organizations.models import Organizition, Teacher
# Create your models here.


class Course(models.Model):
    organization = models.ForeignKey(Organizition, blank=True, null= True, verbose_name= 'course related organization')
    name = models.CharField(max_length=50, verbose_name=u"name of the course")
    desc = models.CharField(max_length=200, verbose_name=u"description of the course")
    detail = models.TextField(verbose_name=u"detail of the course")
    degree = models.CharField(max_length=20,
                              choices=(("Easy", "easy level course"),
                                       ("Medium", "medium level course"),
                                       ("Hard", "hard level of course")),
                              verbose_name=u"difficulty level of degree")
    learn_time = models.IntegerField(default=0, verbose_name=u"length of the course")
    students = models.IntegerField(default=0, verbose_name="number of student")
    like_nums = models.IntegerField(default=0, verbose_name="number of likes")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name=u"cover image", max_length= 100,
                              default='courses/%Y/%m/default.jpg')
    click_nums = models.IntegerField(default=0, verbose_name=u"number of click")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"time of creation of course")
    category = models.CharField(default='backend', max_length=50, verbose_name='category of the course')
    tag = models.CharField(default='', max_length=50, verbose_name='tag of the course')

    teacher = models.ForeignKey(Teacher, blank=True, null= True, verbose_name= 'course related teacher')
    prequist = models.CharField(default='', max_length=50, verbose_name='preqrust for the course')
    goal =  models.CharField(default='', max_length=50, verbose_name='goal of the course')
    is_banner = models.BooleanField(default=False, verbose_name='whether the course will be in banner')

    class Meta:
        verbose_name = u"courses"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_lectures_num(self):
        all_lectures_num = self.lecture_set.all().count()
        return all_lectures_num

    def get_user_course(self):
        user_course = self.usercourse_set.all()[:5]
        return user_course

    def get_lectures(self):
        return self.lecture_set.all()


class Lecture(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"course")
    name = models.CharField(max_length=100, verbose_name=u"lecture name")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"time of lecture added")

    class Meta:
        verbose_name = u"lecutre"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return "{} {}".format(self.course, self.name)

    def get_videos(self):
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lecture, verbose_name=u"lesson")
    name = models.CharField(max_length= 100, verbose_name=u"video name")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"time of video added")
    url = models.URLField(default='', verbose_name='video url')
    video_length = models.IntegerField(default=0, verbose_name=u"length of the video")

    class Meta:
        verbose_name = u"video"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return "{} {}".format(self.lesson, self.name)


class CourseRsource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"course")
    name = models.CharField(max_length=100, verbose_name=u"source name")
    download = models.FileField(upload_to="course/resource/%Y/%m", max_length=100)
    add_time = models.DateTimeField(default= datetime.now, verbose_name=u"time of source added")

    class Meta:
        verbose_name = u"course resource"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return "{} {}".format(self.course, self.name)
