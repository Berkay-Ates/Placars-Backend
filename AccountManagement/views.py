import json

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import AccountManagement.models
from .models import *
from .serializers import *
import requests
from django.contrib.auth.hashers import make_password , check_password
from .utils import generate_access_token,check_access_token,sendMail
from django.core import serializers
import jwt
from django.conf import settings
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponse

"""
apiKey: "AIzaSyCtZuyseegQ5qBVmm-zTC_LjDNld5zS-tg",

  authDomain: "placars-d9bbf.firebaseapp.com",

  projectId: "placars-d9bbf",

  storageBucket: "placars-d9bbf.appspot.com",

  messagingSenderId: "323561976776",

  appId: "1:323561976776:web:54ade11c6a66a3e28d86fd",

  measurementId: "G-LMX73QMGEF"


"""








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
                if instance.isAcitve==False:
                    token = generate_access_token(instance)
                    sendMail(instance.email, token)
                    return  Response('Hesabiniza onay maili gonderilmistir',status=status.HTTP_406_NOT_ACCEPTABLE)
            except Account.DoesNotExist:
                #Yeni Kullanici Olusuturuldu
                instance=Account(name=serializer.validated_data['name'], email=serializer.validated_data.get('email', None),\
                                userIp=get_ip(request),phone=serializer.validated_data.get('phone', None),
                                password=make_password(serializer.validated_data['password']),username=serializer.validated_data['username']
                                ,photo_location=serializer.validated_data.get('email', None))
                print(instance)
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
        sendMail(instance.email,token)
        instance.save()
        account_session.save()
        return Response(token, status=status.HTTP_201_CREATED)
    except Exception as ex:
        print(str(ex))
        raise ex

@api_view(['GET'])
def login(request):
    try:

        serializer=LoginSerializer(data=request.data) # gonderilen istekteki gelen verinin uygun olup olmadigi kontrol ediliyork
        if serializer.is_valid():
            email=serializer.validated_data.get('email', None)
            password=serializer.validated_data.get('password', None)
            try:
                instance=Account.objects.get(email=email)
            except Account.DoesNotExist:
                return Response("Bu maile ait kullanici bulunamamktadir",status.HTTP_404_NOT_FOUND)
            
            if check_password(password=password,encoded=instance.password):
                token=generate_access_token(instance)
                account_session=AccountSession(account_uid=instance.account_uid,name=instance.name,userIp=get_ip(request))
                token['isAcitve']=instance.isAcitve
                return Response(token, status=status.HTTP_202_ACCEPTED)
        else:
            return Response("Gonderilen veriler uygun degil",status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        raise e
        

@api_view(["GET"])
def getAccount(request):
        try:
            decoded=check_access_token(request=request)
            account_uid=decoded['account_uid']
            instance = Account.objects.get(account_uid=account_uid)

            result_dict = {
                'name': instance.name,
                'username': instance.username,
                'phone': instance.phone,
                'isActive': instance.isAcitve,
                'following': instance.following.values_list('username', flat=True),
                'photo_location':instance.photo_location,
            }

            s_instance = serializers.serialize('json', [instance])


            return Response(result_dict,status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            raise e


@api_view(["POST"])
def newCar(request):
    try:
        decoded=check_access_token(request=request)
        account_uid=decoded['account_uid']
        instance: Car= None
        serializer=CarSerializer(data=request.data)
        print(serializer,serializer.is_valid())
        if serializer.is_valid():
            try:
                instance=Car.objects.get(license=serializer.validated_data["license"])            
            except Car.DoesNotExist:

                instance=Car(license=serializer.validated_data["license"],
                             brand=serializer.validated_data.get('brand', None),model=serializer.validated_data.get('model', None),
                             carPhotoLocationNo=serializer.validated_data.get('carPhotoLocationNo', None),carLicensePhotoLocationNo=serializer.validated_data.get('carLicensePhotoLocationNo', None),
                             color=serializer.validated_data.get('color', None),satilikMi=serializer.validated_data.get('satilikMi', None),carKm=serializer.validated_data.get('carKm', None))
                
                if  request.data.get("owner")=="True":
                        account=Account.objects.get(account_uid=account_uid)
                        instance.account=account



                instance.save()



                return Response("Yeni arac olusturuldu", status=status.HTTP_201_CREATED)
            
            return Response("Bu arac kayitlidir", status=status.HTTP_302_FOUND)
        else:
            print('serializer valid degil')
            return Response('Bad Request',status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(e)
        raise e

@api_view(["GET"])
def emailVerify(request,token):
    print("verify email token ",token)
    try:
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256', ])

        account_uid = decoded['account_uid']
        instance = Account.objects.get(account_uid=account_uid)
        instance.isAcitve=True
        instance.save()

        return Response("Onaylandı", status.HTTP_200_OK)

    except Exception as e:
        print(e)
        raise e

@api_view(["GET"])
def getMyCars(request):
    decoded = check_access_token(request=request)
    account_uid = decoded['account_uid']
    account=Account.objects.get(account_uid=account_uid)
    cars = list(Car.objects.filter(account=account))
    cars = serializers.serialize('json', cars)
    return  HttpResponse(cars, content_type='application/json')


@api_view(["GET"])
def CarDetails(request,license):
    try:
        check_access_token(request=request)
        print( "Plaka" ,license)
        car=Car.objects.get(license=license)
        print(car)
        s_car = serializers.serialize('json', [car])
        print(s_car)

    except AccountManagement.models.Car.DoesNotExist:
        return HttpResponse("Böyle bir araç yok", status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        #return HttpResponse("Kullanıcı girişi yapılmalı",status=status.HTTP_401_UNAUTHORIZED)
        print(e)
        raise e

    return  HttpResponse(s_car, content_type='application/json')

@api_view(["POST"])
def newComment(request):
    decoded = check_access_token(request=request)
    account_uid = decoded['account_uid']
    serializer = CommentSerializer(data=request.data)
    print(serializer,serializer.is_valid())
    try:
        if serializer.is_valid():
            Car_license=request.data.get('targetCarLicense')
            print(Car_license)
            car=Car.objects.get(license=Car_license)

            print(car)
            account=Account.objects.get(account_uid=account_uid)
            newComment=Comment(author=account,targetCar=car,
                               content=serializer.validated_data['content'],
                               title=serializer.validated_data['title'])
            newComment.save()


        else:
            return HttpResponse('Seriliazer valid değil', status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(e)
        raise  e

    return  HttpResponse('Oluşturuldı',status=status.HTTP_201_CREATED)


@api_view(["GET"])
def checkMail(request,email):
    accont=Account.objects.filter(email__exact=email)
    print(accont.__len__())
    response={
        "exist":bool(accont.__len__())
    }
    return Response(response)

@api_view(["GET"])
def checkUsername(request,username):
    accont=Account.objects.filter(username__exact=username)
    print(accont.__len__())
    response={
        "exist":bool(accont.__len__())
    }
    return Response(response)














