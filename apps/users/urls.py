from django.conf.urls import url


from .views import UserInfoView, UserImageView, UserPwdUpdate

urlpatterns = [

    url(r'^info/$', UserInfoView.as_view(), name='user_info'),
    url(r'^image/upload/$', UserImageView.as_view(), name='image_upload'),
    url(r'^update/pwd/$', UserPwdUpdate.as_view(), name='update_pwd')

]
