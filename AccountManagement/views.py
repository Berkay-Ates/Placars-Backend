from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Account,AccountSession
from .serializers import AccountSerializer
import requests
from django.contrib.auth.hashers import make_password
from .utils import generate_access_token



def get_geoLocation(ip):
    response = requests.get(f'https://ipapi.co/{ip}/json/').json()
    try:
        if response['error'] == True:
            return False
    except:
        return response



def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    else:
        return request.META.get('REMOTE_ADDR')


@api_view(['POST'])
def createAccount(request):
    try:

        serializer=AccountSerializer(data=request.data) # gonderilen istekteki gelen verinin uygun olup olmadigi kontrol ediliyork

        instance: Account =None
        if serializer.is_valid():
            try:
                instance=Account.objects.get(email=serializer.validated_data['email'])
                return  Response('Bu mail kullanilmaktadir',status=status.HTTP_406_NOT_ACCEPTABLE)
            except Account.DoesNotExist:
                #Yeni Kullanici Olusuturuldu
                instance=Account(name=serializer.validated_data['name'], email=serializer.validated_data.get('email', None),\
                                userIp=get_ip(request),phone=serializer.validated_data['phone'],
                                password=make_password(serializer.validated_data['password']))
        else:
            print('serializer valid degil')
            return Response('Bad Request',status=status.HTTP_400_BAD_REQUEST)

        account_session=AccountSession(account_uid=instance.account_uid,name=instance.name,userIp=get_ip(request))

        if serializer.validated_data.get('userIp',None) is not None:
            geo_data = get_geoLocation(instance.userIp)


            if geo_data is not None:
                if 'latitude' in geo_data:
                    instance.latitude=geo_data['latitude']
                    account_session.latitude=geo_data['latitude']
                if 'longitude' in geo_data:
                    instance.longitude=geo_data['longitude']
                    account_session.latitude=geo_data['longitude']



        
        token=generate_access_token(instance)
        instance.save()
        account_session.save()
        return Response(token, status=status.HTTP_201_CREATED)
    except Exception as ex:
        print(str(ex))
        raise ex

@api_view(['GET'])
def login(request):
    pass












