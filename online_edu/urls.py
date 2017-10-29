"""online_edu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve
import xadmin

from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ActiveResetView, PassWordResetView
from users.views import LogoutView, IndexView
from organizations.views import OrgView
from settings import MEDIA_ROOT, STATIC_ROOT

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),

    url(r'^$', IndexView.as_view(), name="index"),
    # url(r'^login/$', user_login, name="login")
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name="register"),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    url(r'^forgetpwd', ForgetPwdView.as_view(), name= "forgetpsd"),
    url(r'^reset/(?P<active_code>.*)/$', ActiveResetView.as_view(), name = 'resetpwd'),
    url(r'^modifypwd', PassWordResetView.as_view(), name='modifypwd'),

    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    url(r'static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
    # url(r'^org-list/$', OrgView.as_view(), name='org_list'),

    # ulrs for the organization app
    url(r'^org/', include('organizations.urls', namespace='org')),

    url(r'^course/', include('courses.urls', namespace='course')),

    url(r'^users/', include('users.urls', namespace='users')),

]

handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'
