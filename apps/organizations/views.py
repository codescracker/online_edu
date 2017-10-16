from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from .models import Organizition, City
from .forms import UserAskForm

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
    def get(self, request):
        org_id = request.GET.get('org_id', 0)

        return render(request, 'org-detail-homepage.html')

