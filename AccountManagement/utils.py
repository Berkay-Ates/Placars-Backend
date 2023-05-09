import datetime
import jwt
from django.conf import settings
import json
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def generate_access_token(user):

    access_token_payload = {
        'account_uid':str(user.account_uid),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, minutes=30),
        'iat': datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload,
                              settings.SECRET_KEY, algorithm='HS256')
    return {"access":access_token}


def check_access_token(request):


    decoded=None
    try:
        token=request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
        decoded=jwt.decode(token,settings.SECRET_KEY, algorithms=['HS256',])
    except jwt.exceptions.ExpiredSignatureError :
            return Response("Token gecerlilik suresini yitirmistir",status.HTTP_401_UNAUTHORIZED)
    
    except jwt.exceptions.DecodeError:
            return Response("Hatali Token",status.HTTP_400_BAD_REQUEST)

         

    return decoded


def sendMail(target,token):
    print("sent amil ")
    html_message = render_to_string('email/emailTemplate.html', {'confirmation_link': 'http://127.0.0.1:8000/AccountManagement/confimEmail/'+token['access']})
    plain_message = strip_tags(html_message)
    send_mail(
        'Onay e-postası',  # konu
        plain_message,  # düz metin içerik
        'settings.EMAIL_HOST_USER',  # gönderen
        [target],  # alıcılar
        html_message=html_message,  # HTML içerik
        fail_silently=False
    )
    print("gönderildi")
