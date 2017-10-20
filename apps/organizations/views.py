from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse


from .models import Organizition, City
from .forms import UserAskForm
from operation.models import UserFavorite

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

import json

# Create your views here.


class OrgView(View):
    def get(self, request):
        all_orgs = Organizition.objects.all()
        all_cities = City.objects.all()

        hot_orgs = all_orgs.order_by('-click_nums')[:5]

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

                    response_data = dict()
                    response_data['status'] = 'success'
                    response_data['msg'] = 'saved'

                    return HttpResponse(json.dumps(response_data), content_type='application/json')
                else:
                    response_data = dict()
                    response_data['status'] = 'fail'
                    response_data['msg'] = 'save error'

                    return HttpResponse(json.dumps(response_data), content_type='application/json')



