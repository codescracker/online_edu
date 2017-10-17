from django.conf.urls import url, include

from organizations.views import OrgView, UserAskView, OrgDetailHomeView, OrgDetailCourseView, OrgDetailTeacherView, \
    OrgDetailIntroView, UserFavView

urlpatterns = [

    url(r'^list/$', OrgView.as_view(), name='org_list'),
    url(r'^add_ask', UserAskView.as_view(), name='user_ask'),
    url(r'^home/(?P<org_id>\d+)/$', OrgDetailHomeView.as_view(), name='home'),
    url(r'^courses/(?P<org_id>\d+)/$', OrgDetailCourseView.as_view(), name='courses'),
    url(r'^teachers/(?P<org_id>\d+)/$', OrgDetailTeacherView.as_view(), name='teachers'),
    url(r'^desc/(?P<org_id>\d+)/$', OrgDetailIntroView.as_view(), name='intro'),

    url(r'^add_fav/$', UserFavView.as_view(), name='add_fav'),

]
