import datetime
import jwt
from django.conf import settings
import json
from rest_framework.response import Response
from rest_framework import status



def generate_access_token(user):

    access_token_payload = {
        'account_uid':str(user.account_uid),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=30),
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