import datetime
import jwt
from django.conf import settings
import json


def generate_access_token(user):

    access_token_payload = {
        'account_uid':str(user.account_uid),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=30),
        'iat': datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload,
                              settings.SECRET_KEY, algorithm='HS256')
    return {"access":access_token}


def check_access_token(token):
    decoded=None
    try:
        decoded=jwt.decode(token,settings.SECRET_KEY, algorithms=['HS256',])
    except jwt.exceptions.ExpiredSignatureError :
        print("Gecerliklik suresi dolmustur")
        
    return decoded