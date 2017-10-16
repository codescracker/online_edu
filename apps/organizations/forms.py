# -*- coding: utf-8 -*-

from django import forms
from operation.models import UserAsk

import re


class UserAskForm(forms.ModelForm):

    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        print mobile
        REX = '^\(?([0-9]{3})\)?[-.●]?([0-9]{3})[-.●]?([0-9]{4})$'
        p = re.compile(REX)
        if p.match(mobile):
            print 'match'
            return mobile
        else:
            print 'not match'
            raise forms.ValidationError('Illigel Phone Number', code='mobile_invalid')
