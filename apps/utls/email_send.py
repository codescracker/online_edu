# -*- coding: utf-8 -*-
from users.models import EmailVerifyRecord
from django.core.mail import send_mail


from online_edu.settings import EMAIL_FROM
import random


def send_register_email(email, send_type='register'):
    email_verification = EmailVerifyRecord()

    code = generate_verificationcode(16)
    email_verification.code = code
    email_verification.email = email
    email_verification.send_type = send_type

    email_verification.save()

    email_title = ''
    email_body = ''

    if send_type == 'register':
        email_title = 'Online Edu activation link'
        email_body = "Please click the link below to activate your account http:/127.0.0.1/8000/active/{}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass


def generate_verificationcode(codelength = 8):
    code_list = []
    pool = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890"
    pool_length = len(pool)

    for i in range(0, codelength):
        code_list.append(pool[random.randint(0, pool_length-1)])

    return ''.join(code_list)

