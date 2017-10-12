# -*- coding: utf-8 -*-

import xadmin
from .models import City, Organizition, Teacher


class CityAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class OrganizationAdmin(object):
    list_display =['city', 'name', 'desc', 'click_nums', 'like_nums', 'address']
    search_fields = ['city', 'name', 'desc', 'click_nums', 'like_nums', 'address']
    list_filter = ['city', 'name', 'desc', 'click_nums', 'like_nums', 'address']


class TeacherAdmin(object):
    list_display = ['organization', 'name', 'work_year', 'work_company', 'points', 'click_nums', 'like_nums', 'add_time']
    search_fields = ['organization', 'name', 'work_year', 'work_company', 'points', 'click_nums', 'like_nums']
    list_filter = ['organization', 'name', 'work_year', 'work_company', 'points', 'click_nums', 'like_nums', 'add_time']


xadmin.site.register(City, CityAdmin)
xadmin.site.register(Organizition,OrganizationAdmin)
xadmin.site.register(Teacher, TeacherAdmin)

