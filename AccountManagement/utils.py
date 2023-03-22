import datetime
import jwt
from django.conf import settings
import json


def generate_access_token(user):

    access_token_payload = {
        'user_id':str(user.account_uid),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=5),
        'iat': datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload,
                              settings.SECRET_KEY, algorithm='HS256')
    return {"access":access_token}
