# -*- coding: utf-8 -*-

from django import forms

from captcha.fields import CaptchaField


class ResetpwdForm(forms.Form):
    newpwd = forms.CharField(required=True, min_length=6, max_length=20)
    cfmpwd = forms.CharField(required=True, min_length=6, max_length=20)


class ForgetPsdForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(required=True)


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(required=True)

