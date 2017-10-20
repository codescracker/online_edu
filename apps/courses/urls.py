from django.conf.urls import url

from .views import CourseView, CourseDetailView, CourseInfoView, CourseCommentView, AddCourseCommentsView

urlpatterns = [

    url(r'^list/$', CourseView.as_view(), name='course_list'),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_info'),
    url(r'comments/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name='course_comments'),
    url(r'^add_comments$', AddCourseCommentsView.as_view(), name='add_comments')
]
