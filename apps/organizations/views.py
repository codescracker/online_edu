from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from django.db.models import Q


from .models import Organizition, City, Teacher
from .forms import UserAskForm
from operation.models import UserFavorite
from courses.models import Course

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

import json

# Create your views here.


class OrgView(View):
    def get(self, request):
        all_orgs = Organizition.objects.all()
        all_cities = City.objects.all()

        hot_orgs = all_orgs.order_by('-click_nums')[:5]

        search_keyword = request.GET.get('keywords', '')
        if search_keyword:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keyword) |
                                       Q(desc__icontains=search_keyword))

        city_id = request.GET.get('city', '')
        org_ct = request.GET.get('ct', '')
        sort_by = request.GET.get('sort', '')

        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        if org_ct:
            all_orgs = all_orgs.filter(category=org_ct)

        if sort_by:
            all_orgs = all_orgs.order_by('-' + sort_by)

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 5, request=request)

        orgs = p.page(page)

        return render(request, 'org-list.html', {
            'orgs': orgs,
            'org_count': all_orgs.count(),
            'all_cities': all_cities,
            'city_id': city_id,
            'org_ct': org_ct,
            'hot_orgs': hot_orgs,
            'sort_by': sort_by
        }
                      )


class UserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            response_data = {}
            response_data['status'] = 'success'
            response_data['msg'] = ''
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            response_data = {}
            response_data['status'] = 'fail'
            response_data['msg'] = 'Add Error'
            return HttpResponse(json.dumps(response_data), content_type="application/json")


class OrgDetailHomeView(View):
    def get(self, request, org_id):
        org = Organizition.objects.get(id=int(org_id))
        org.click_nums += 1
        org.save()

        has_save = False
        if request.user.is_authenticated() and UserFavorite.objects.filter(user=request.user, fav_id=org.id,
                                                                           fav_type=2):
            has_save = True

        print has_save
        all_courses = org.course_set.all()[:3]
        all_teachers = org.teacher_set.all()[:2]
        return render(request, 'org-detail-homepage.html',
                      {'all_courses': all_courses, 'all_teachers': all_teachers, 'org': org, 'current_page': 'home',
                       'has_save': has_save})


class OrgDetailCourseView(View):
    def get(self, request, org_id):
        org = Organizition.objects.get(id=int(org_id))
        has_save = False
        if request.user.is_authenticated() and UserFavorite.objects.filter(user=request.user, fav_id=org.id,
                                                                           fav_type=2):
            has_save = True

        all_courses = org.course_set.all()
        return render(request, 'org-detail-course.html',
                      {'all_courses': all_courses,  'org': org, 'current_page': 'course', 'has_save': has_save})


class OrgDetailTeacherView(View):
    def get(self, request, org_id):
        org = Organizition.objects.get(id=int(org_id))
        has_save = False
        if request.user.is_authenticated() and UserFavorite.objects.filter(user=request.user, fav_id=org.id,
                                                                           fav_type=2):
            has_save = True
        all_teachers = org.teacher_set.all()
        return render(request, 'org-detail-teachers.html',
                      {'all_teachers': all_teachers, 'org': org, 'current_page': 'teacher', 'has_save': has_save})


class OrgDetailIntroView(View):
    def get(self, request, org_id):
        org = Organizition.objects.get(id=int(org_id))
        has_save = False
        if request.user.is_authenticated() and UserFavorite.objects.filter(user=request.user, fav_id=org.id,
                                                                           fav_type=2):
            has_save = True
        return render(request, 'org-detail-desc.html', {'org': org, 'current_page': 'intro', 'has_save': has_save})


class UserFavView(View):
    def post(self, request):
        fav_id = int(request.POST.get('fav_id', 0))
        fav_type = int(request.POST.get('fav_type', 0))

        if not request.user.is_authenticated():
            response_data = dict()
            response_data['status'] = 'fail'
            response_data['msg'] = 'user not log in'
            print 'user not log in'
            return HttpResponse(json.dumps(response_data), content_type='application/json')
        else:
            user_id = request.user.id

            exist_record = UserFavorite.objects.filter(user=user_id, fav_id=fav_id, fav_type=fav_type)
            if exist_record:
                exist_record.delete()
                if fav_type == 1:
                    course = Course.objects.get(id=fav_id)
                    course.like_nums -= 1
                    if course.like_nums < 0:
                        course.like_nums = 0
                    course.save()
                if fav_type == 2:
                    org = Organizition.objects.get(id=fav_id)
                    org.like_nums -= 1
                    if org.like_nums < 0:
                        org.like_nums = 0
                    org.save()
                if fav_type == 3:
                    teacher = Teacher.objects.get(id=fav_id)
                    teacher.like_nums -= 1
                    if teacher.like_nums < 0:
                        teacher.like_nums = 0
                    teacher.save()

                response_data = dict()
                response_data['status'] = 'success'
                response_data['msg'] = 'save'
                return HttpResponse(json.dumps(response_data), content_type='application/json')
            else:
                user_fav = UserFavorite()
                if fav_id > 0 and fav_type > 0:
                    user_fav.user_id = user_id
                    user_fav.fav_id = fav_id
                    user_fav.fav_type = fav_type
                    user_fav.save()

                    if fav_type == 1:
                        course = Course.objects.get(id=fav_id)
                        course.like_nums += 1
                        course.save()
                    if fav_type == 2:
                        org = Organizition.objects.get(id=fav_id)
                        org.like_nums += 1
                        org.save()
                    if fav_type == 3:
                        teacher = Teacher.objects.get(id=fav_id)
                        teacher.like_nums += 1
                        teacher.save()

                    response_data = dict()
                    response_data['status'] = 'success'
                    response_data['msg'] = 'saved'

                    return HttpResponse(json.dumps(response_data), content_type='application/json')
                else:
                    response_data = dict()
                    response_data['status'] = 'fail'
                    response_data['msg'] = 'save error'

                    return HttpResponse(json.dumps(response_data), content_type='application/json')


class TeacherListView(View):
    def get(self, request):
        all_teachers = Teacher.objects.all()
        teachers_rank = Teacher.objects.all().order_by('-click_nums')[:4]

        search_keyword = request.GET.get('keywords', '')
        if search_keyword:
            all_teachers = all_teachers.filter(Q(name__icontains=search_keyword) |
                                               Q(work_company__icontains=search_keyword) |
                                               Q(work_position__icontains=search_keyword))

        sort = request.GET.get('sort', '')
        if sort:
            print sort
            all_teachers = all_teachers.order_by('-'+sort)

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teachers, 3, request=request)

        teachers = p.page(page)
        data = dict()
        data['teachers'] = teachers
        data['order'] = sort
        data['teachers_rank'] = teachers_rank
        data['teachers_count'] = all_teachers.count()
        return render(request, 'teachers-list.html', data)


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        all_courses = teacher.course_set.all()
        org = teacher.organization
        teachers_rank = Teacher.objects.all().order_by('-click_nums')[:4]

        is_teacher_saved = False
        is_org_saved = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(fav_id=teacher_id, fav_type=3, user=request.user):
                is_teacher_saved = True
            if UserFavorite.objects.filter(fav_id=org.id, fav_type=2, user=request.user):
                is_org_saved = True

        data = dict()
        data['teacher'] = teacher
        data['all_courses'] = all_courses
        data['org'] = org
        data['hot_teachers'] = teachers_rank
        data['is_teacher_saved'] = is_teacher_saved
        data['is_org_saved'] = is_org_saved
        return render(request, 'teacher-detail.html', data)


















