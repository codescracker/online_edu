from django.conf.urls import url, include

from organizations.views import OrgView, UserAskView, OrgDetailHomeView

urlpatterns = [

    url(r'^list/$', OrgView.as_view(), name='org_list'),
    url(r'^add_ask', UserAskView.as_view(), name='user_ask'),
    url(r'^org-detail-home/&', OrgDetailHomeView.as_view(), name='org_detail_home')
]
