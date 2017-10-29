from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetPsdForm, ResetpwdForm, ImageForm, UserInfoForm
from utls.email_send import send_register_email
from operation.models import UserCourse, UserFavorite, UserMessage
from organizations.models import Organizition, Teacher
from courses.models import Course
from users.models import Banner

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
import json
# Create your views here.


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class PassWordResetView(View):
    def post(self, request):
        reset_form = ResetpwdForm(request.POST)
        email = request.POST.get('email')
        if reset_form.is_valid():
            new_pwd = request.POST.get('password')
            confirm_pwd = request.POST.get('password2')
            if new_pwd == confirm_pwd:
                user = UserProfile.objects.get(email=email)
                user.password = make_password(new_pwd)
                user.save()
                return render(request, "password_reset.html", {'msg': 'new passwrod is set, please log in',
                                                               "reset": reset_form,
                                                               "isfinish": 'Yes',
                                                               "email": email})
            else:
                return render(request, "password_reset.html", {'msg': 'Please check the new password',
                                                               "reset": reset_form,
                                                               "isfinish": 'No',
                                                                "email" : email})
        else:
            return render(request, "password_reset.html", {'msg': 'Please input required format of password',
                                                           "reset": reset_form,
                                                           "isfinish": 'No',
                                                           "email": email})


class ActiveResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code = active_code)
        if all_records:
            for record in all_records:
                if record.send_type == 'forget':
                    email = record.email
                    return render(request, 'password_reset.html', {'email': email, "isfinish": 'No'})
        else:
            return render(request, 'wrong-activecode.html')


class ForgetPwdView(View):
    def get(self, request):
        forgetpwd_form = ForgetPsdForm()
        return render(request, "forgetpwd.html", {"forgetpwd_form": forgetpwd_form})

    def post(self, request):
        forgetpwd_form = ForgetPsdForm(request.POST)
        if forgetpwd_form.is_valid():
            email = request.POST.get('email')
            all_records = UserProfile.objects.filter(email=email)
            if all_records:
                send_register_email(email, 'forget')
                return render(request, "forgetpwd.html", {'msg': 'Verification Code sent to email already'})
            else:
                return render(request, "forgetpwd.html", {'msg': 'Please input correct email\captcha', 'forgetpwd_form':forgetpwd_form})
        else:
            return render(request, "forgetpwd.html", {"forgetpwd_form": forgetpwd_form})


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        return render(request, "login.html")


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {"register_form": register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get("email")
            if UserProfile.objects.filter(email= email):
                return render(request, "register.html", {"register_form": register_form, "msg": "User already exist"})
            password = request.POST.get("password")
            user_profile = UserProfile()
            user_profile.email = email
            user_profile.username = email
            user_profile.password = make_password(password)
            user_profile.is_active = False
            user_profile.save()

            user_msg = UserMessage()
            user_msg.user_id = user_profile.id
            user_msg.message = "Welcome to the Online Edu"
            user_msg.save()

            send_register_email(email, 'register')
            return render(request, "login.html")
        else:
            return render(request, "register.html", {"register_form": register_form})


class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")

            user = authenticate(username=user_name, password=pass_word)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': 'user is not activated yet', 'login_form': login_form})
            else:
                return render(request, "login.html",
                              {'msg': "Username/email or password is incorrect", 'login_form': login_form})
        else:
            return render(request, "login.html", {'login_form': login_form})

#### function style view ####
# def user_login(request):
#     if request.method == "POST":
#         user_name = request.POST.get("username", "")
#         pass_word = request.POST.get("password", "")
#
#         user = authenticate(username=user_name, password=pass_word)
#         if user:
#             login(request, user)
#             return render(request, 'index.html')
#         else:
#             return render(request, "login.html", {'msg': "Username/email or password is incorrect"})
#
#     elif request.method == "GET":
#         return render(request, "login.html", {})


class LogoutView(View):
    def get(self, request):
        logout(request)

        return HttpResponseRedirect(reverse('index'))


class UserInfoView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return render(request, 'login.html')

        data = dict()
        data['userprofile'] = request.user
        return render(request, 'usercenter-info.html', data)

    def post(self, request):
        if not request.user.is_authenticated():
            return render(request, 'login.html')

        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            response_data = dict()
            response_data['status'] = 'success'
            return HttpResponse(json.dumps(response_data), content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UserImageView(View):
    def post(self, request):
        image_form = ImageForm(request.POST, request.FILES)
        if image_form.is_valid():
            image = image_form.cleaned_data['image']
            request.user.image = image
            request.user.save()

            response_data = dict()
            response_data['status'] = 'success'
            return HttpResponse(json.dumps(response_data), content_type='application/json')
        else:
            response_data = dict()
            response_data['status'] = 'fail'
            return HttpResponse(json.dumps(response_data), content_type='application/json')


class UserPwdUpdate(View):
    def post(self, request):
        update_form = ResetpwdForm(request.POST)
        if update_form.is_valid():
            newpwd = request.POST.get('newpwd')
            cfmpwd = request.POST.get('cfmpwd')
            if newpwd != cfmpwd:
                response_data = dict()
                response_data['status'] = 'fail'
                response_data['msg'] = 'two passwords are not consistent'
                return HttpResponse(json.dumps(response_data), content_type='application/json')
            else:
                request.user.password = make_password(newpwd)
                request.user.save()
                response_data = dict()
                response_data['status'] = 'success'
                return HttpResponse(json.dumps(response_data), content_type='application/json')
        else:
            response_data = dict()
            response_data['status'] = 'fail'
            response_data['msg'] = 'Please check the format of the passwords'
            return HttpResponse(json.dumps(response_data), content_type='application/json')


class SendEmailCodeView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return render(request, 'index.html')

        email = request.GET.get('email', '')
        print email
        if UserProfile.objects.filter(email=email):
            print 'exist'
            response_data = dict()
            response_data['email'] = 'The Email already exists'
            return HttpResponse(json.dumps(response_data), content_type='application/json')

        send_register_email(email, 'update')
        response_data = dict()
        response_data['status'] = 'success'
        return HttpResponse(json.dumps(response_data), content_type='application/json')


class UpdateEmailView(View):
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        existed_verification_records = EmailVerifyRecord.objects.filter(email= email, code=code, send_type='update')

        if existed_verification_records:
            user = request.user
            user.email = email
            user.save()

            response_data = dict()
            response_data['status'] = 'success'

            return HttpResponse(json.dumps(response_data), content_type='application/json')

        else:
            response_data = dict()
            response_data['email'] = 'Please input correct verification codes'
            return HttpResponse(json.dumps(response_data), content_type='application/json')


class MyCourseView(View):
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)

        data = dict()
        data['user_courses'] = user_courses

        return render(request, 'usercenter-mycourse.html', data)


class MyFavOrgView(View):
    def get(self, request):
        fav_orgs = []
        for user_fav in UserFavorite.objects.filter(user=request.user, fav_type=2):
            fav_org_id = user_fav.fav_id
            fav_org = Organizition.objects.get(id = fav_org_id)
            fav_orgs.append(fav_org)

        data = dict()
        data['fav_orgs'] = fav_orgs

        return render(request, 'usercenter-fav-org.html', data)


class MyFavTeacherView(View):
    def get(self, request):
        fav_teachers = []
        for user_fav in UserFavorite.objects.filter(user=request.user, fav_type=3):
            fav_teacher_id = user_fav.fav_id
            fav_teacher = Teacher.objects.get(id = fav_teacher_id)
            fav_teachers.append(fav_teacher)

        data = dict()
        data['fav_teachers'] = fav_teachers

        return render(request, 'usercenter-fav-teacher.html', data)


class MyFavCourseView(View):
    def get(self, request):
        fav_courses = []
        for user_fav in UserFavorite.objects.filter(user=request.user, fav_type=1):
            fav_course_id = user_fav.fav_id
            fav_course = Course.objects.get(id = fav_course_id)
            fav_courses.append(fav_course)

        data = dict()
        data['fav_courses'] = fav_courses

        return render(request, 'usercenter-fav-course.html', data)


class MyMsgView(View):
    def get(self, request):
        user_id = request.user.id

        all_msgs = UserMessage.objects.filter(user_id=user_id)
        all_unread_msgs = UserMessage.objects.filter(user_id=user_id, has_read=False)

        for unread_msg in all_unread_msgs:
            unread_msg.has_read = True
            unread_msg.save()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_msgs, 5, request=request)

        msgs = p.page(page)

        data = dict()
        data['msgs'] = msgs

        return render(request, 'usercenter-message.html', data)


class IndexView(View):
    def get(self, request):
        all_banner_images = Banner.objects.all().order_by('index')

        all_courses = Course.objects.all()

        courses_banners = all_courses.filter(is_banner=True)[:3]
        courses_notbanners = all_courses.filter(is_banner=False)[:6]

        all_orgs = Organizition.objects.all().order_by('-click_nums')[:12]

        data = dict()
        data['all_banner_images'] = all_banner_images
        data['courses_banners'] = courses_banners
        data['courses_notbanners'] = courses_notbanners
        data['all_orgs'] = all_orgs

        return render(request, 'index.html', data)


def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
