# -*- coding: utf-8 -*-

import xadmin
from .models import Course, Lecture, Video, CourseRsource


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_time',
                    'students', 'like_nums', 'image', 'click_nums', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_time',
                     'students', 'like_nums', 'image', 'click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_time',
                   'students', 'like_nums', 'image', 'click_nums', 'add_time']


class LectureAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseRsoourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course', 'name', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lecture, LectureAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseRsource, CourseRsoourceAdmin)
