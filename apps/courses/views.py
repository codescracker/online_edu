from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from django.db.models import Q

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Course, CourseRsource
from operation.models import UserFavorite, CourseComments, UserCourse
from users.models import UserProfile

import json

# Create your views here.


class CourseView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')

        hot_courses = Course.objects.all().order_by('-click_nums')[:3]

        search_keyword = request.GET.get('keywords', '')
        if search_keyword:
            all_courses = all_courses.filter(Q(name__icontains=search_keyword) |
                                             Q(desc__icontains=search_keyword) |
                                             Q(detail__icontains=search_keyword))

        order = request.GET.get('sort', '')
        if order:
            all_courses = all_courses.order_by('-'+order)

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 3, request=request)

        courses = p.page(page)

        data = dict()
        data['courses'] = courses
        data['order'] = order
        data['hot_courses'] = hot_courses
        return render(request, 'course-list.html', data)


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        tag = course.tag
        if tag:
            related_courses = Course.objects.filter(tag=tag)[:2]
        else:
            related_courses = []

        has_course_save = False
        has_org_save = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_course_save = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.organization.id, fav_type =2):
                has_org_save = True

        data = dict()
        data['course'] = course
        data['related_courses'] = related_courses
        data['has_course_save'] = has_course_save
        data['has_org_save'] = has_org_save
        return render(request, 'course-detail.html', data)


class CourseInfoView(View):
    def get(self, request, course_id):
        if not request.user.is_authenticated():
            return render(request, 'login.html')

        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()

        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            new_user_course = UserCourse()
            new_user_course.course = course
            new_user_course.user = request.user
            new_user_course.save()

        resources = CourseRsource.objects.filter(course=course)

        all_users_courses = UserCourse.objects.filter(course=course)
        all_users = [user_course.user for user_course in all_users_courses]
        all_related_courses = set()
        for user in all_users:
            related_user_courses = UserCourse.objects.filter(user=user)
            for related_user_course in related_user_courses:
                all_related_courses.add(related_user_course.course)

        data = dict()
        data['courses'] = course
        data['resources'] = resources
        data['all_related_courses'] = list(all_related_courses)[:5]
        return render(request, 'course-video.html', data)


class CourseCommentView(View):
    def get(self, request, course_id):
        if not request.user.is_authenticated():
            return render(request, 'login.html')

        course = Course.objects.get(id=int(course_id))
        comments = CourseComments.objects.filter(course=course)

        resources = CourseRsource.objects.filter(course=course)

        all_users_courses = UserCourse.objects.filter(course=course)
        all_users = [user_course.user for user_course in all_users_courses]
        all_related_courses = set()
        for user in all_users:
            related_user_courses = UserCourse.objects.filter(user=user)
            for related_user_course in related_user_courses:
                all_related_courses.add(related_user_course.course)

        data = dict()
        data['comments'] = comments
        data['courses'] = course
        data['resources'] = resources
        data['all_related_courses'] = list(all_related_courses)[:5]

        return render(request, 'course-comment.html', data)


class AddCourseCommentsView(View):
    def post(self, request):
        if not request.user.is_authenticated():
            return render(request, 'login.html')

        course_id = int(request.POST.get('course_id', 0))
        comment = request.POST.get('comments', '')

        if not request.user.is_authenticated():
            response_data = dict()
            response_data['status'] = 'fail'
            response_data['msg'] = 'user not log in'
            print 'user not log in'
            return HttpResponse(json.dumps(response_data), content_type='application/json')
        else:
            if course_id > 0 and comment:
                user_id = request.user.id
                course_comment = CourseComments()

                user = UserProfile.objects.get(id=user_id)
                course = Course.objects.get(id=course_id)
                course_comment.user = user
                course_comment.course = course
                course_comment.comments = comment

                course_comment.save()

                response_data = dict()
                response_data['status'] = 'success'
                response_data['msg'] = 'saved'

                return HttpResponse(json.dumps(response_data), content_type='application/json')
            else:
                response_data = dict()
                response_data['status'] = 'fail'
                response_data['msg'] = 'save error'

                return HttpResponse(json.dumps(response_data), content_type='application/json')


