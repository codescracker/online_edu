from django.conf.urls import url


from .views import UserInfoView, UserImageView, UserPwdUpdate, SendEmailCodeView, UpdateEmailView, MyCourseView
from .views import MyFavOrgView, MyFavTeacherView, MyFavCourseView, MyMsgView


urlpatterns = [

    url(r'^info/$', UserInfoView.as_view(), name='user_info'),
    url(r'^image/upload/$', UserImageView.as_view(), name='image_upload'),
    url(r'^update/pwd/$', UserPwdUpdate.as_view(), name='update_pwd'),
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name='send_email_code'),
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),
    url(r'^my_course/$', MyCourseView.as_view(), name='my_courses'),
    url(r'^fav/orgs/$', MyFavOrgView.as_view(), name='my_fav_orgs'),
    url(r'^fav/teachers/$', MyFavTeacherView.as_view(), name='my_fav_teachers'),
    url(r'^fav/courses/$', MyFavCourseView.as_view(), name='my_fav_courses'),
    url(r'^messages/$', MyMsgView.as_view(), name='my_msg'),
]
