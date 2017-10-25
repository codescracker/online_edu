from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetPsdForm, ResetpwdForm, ImageForm
from utls.email_send import send_register_email


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

            send_register_email(email, 'register')
            return render(request, "login.html")
        else:
            print 'haha'
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
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {'msg': 'user is not activated yet'})
            else:
                return render(request, "login.html", {'msg': "Username/email or password is incorrect"})
        else:
            return render(request, "login.html", {'login_form': login_form})


def user_login(request):
    if request.method == "POST":
        user_name = request.POST.get("username", "")
        pass_word = request.POST.get("password", "")

        user = authenticate(username=user_name, password=pass_word)
        if user:
            login(request, user)
            return render(request, 'index.html')
        else:
            return render(request, "login.html", {'msg': "Username/email or password is incorrect"})

    elif request.method == "GET":
        return render(request, "login.html", {})


class UserInfoView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return render(request, 'login.html')

        data = dict()
        data['userprofile'] = request.user
        return render(request, 'usercenter-info.html', data)


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
