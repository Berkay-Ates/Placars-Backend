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
                    return  Response(token,status=status.HTTP_201_CREATED)

                else:
                    return Response('Hesabiniz Kayitlidir.', status=status.HTTP_200_OK)
            except Account.DoesNotExist:
                #Yeni Kullanici Olusuturuldu
                instance=Account(name=serializer.validated_data['name'], email=serializer.validated_data.get('email', None),\
                                userIp=get_ip(request),phone=serializer.validated_data.get('phone', None),
                                password=make_password(serializer.validated_data['password']),username=serializer.validated_data['username']
                                ,profile_img_url=serializer.validated_data.get('profile_img_url', None))
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
                token['username']=instance.username
                token['email']=instance.email
                token['isAcitve']=instance.isAcitve
                token['profile_img_url']=instance.profile_img_url
                token['name']=instance.name


                return Response(token, status=status.HTTP_202_ACCEPTED)
        else:
            return Response("Gonderilen veriler uygun degil",status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        raise e
        

@api_view(["GET"])
def view_account(request):
        try:
            email=request.data.get("email")

            instance = Account.objects.get(email__exact=email)

            result_dict = {
                'name': instance.name,
                'username': instance.username,
                'phone': instance.phone,
                'isActive': instance.isAcitve,
                'following': instance.following.values_list('email', flat=True),
                'profile_img_url':instance.profile_img_url,
                'email':instance.email,
                'recently_messaged': instance.recently_messaged.values_list('email', flat=True),
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
        if serializer.is_valid():
            try:
                instance=Car.objects.get(carPlate=serializer.validated_data["carPlate"])
            except Car.DoesNotExist:

                instance=Car(carPlate=serializer.validated_data["carPlate"],
                             carBrand=serializer.validated_data.get('carBrand', None),carPhotoUrl=serializer.validated_data.get('carPhotoUrl', None),
                             carLicencePhotoUrl=serializer.validated_data.get('carLicencePhotoUrl', None),
                             carKm=serializer.validated_data.get('carKm', None),carDescription=serializer.validated_data.get('carDescription', None)
                             ,carCommentCount=serializer.validated_data.get('carCommentCount', None)
                             ,carLikeCount=serializer.validated_data.get('carLikeCount', None))
                
                if  request.data.get("owner")=="True":
                        account=Account.objects.get(account_uid=account_uid)
                        instance.account=account


                if request.data.get("isCarSale")=="True":
                    instance.isCarSale=True




                instance.save()



                return Response("Yeni arac olusturuldu", status=status.HTTP_201_CREATED)
            
            return Response("Bu arac kayitlidir", status=status.HTTP_302_FOUND)
        else:
            print('serializer valid degil')
            return Response('Bad Request',status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(e)
        raise e

@api_view(["POST"])
def deleteCar(request):
    try:
        decoded=check_access_token(request=request)
        account_uid=decoded['account_uid']

        account=Account.objects.get(account_uid=account_uid)

        car=Car.objects.get(carPlate=request.data.get("carPlate"))

        if car.account==account:
            car.delete()
        else:
            return Response("Bu araci silemezsiniz",status=status.HTTP_403_FORBIDDEN)


    except Exception as e :
        print(e)
        raise e

    return Response("Arac silinmistir",status=status.HTTP_200_OK)






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
    cars = list(Car.objects.filter(account__exact=account))
    response = []

    for car in cars:
        response.append({

            "carOwnerEmail": car.account.email,
            "carPlate": car.carPlate,
            "carBrand": car.carBrand,
            "carPhotoUrl": car.carPhotoUrl,
            "isCarSale": car.isCarSale,
            "carKm": car.carKm,
            "carDescription": car.carDescription,
            "carLicencePhotoUrl": car.carLicencePhotoUrl,
            "carCommentCount": car.carCommentCount,
            "carLikeCount": car.carLikeCount,
            "postDate":car.postDate,
            "profile_img_url": account.profile_img_url

        })



    return  Response({"cars":response}, status=status.HTTP_200_OK)


@api_view(["GET"])
def CarDetails(request,carPlate):
    try:
        check_access_token(request=request)
        print( "Plaka" ,carPlate)
        car=Car.objects.get(carPlate=carPlate)
        account=car.account
        print(car)

        response={
            "carOwnerEmail": car.account.email,
            "carPlate": car.carPlate,
            "carBrand": car.carBrand,
            "carPhotoUrl": car.carPhotoUrl,
            "postDate": car.postDate,
            "isCarSale": car.isCarSale,
            "carKm": car.carKm,
            "carDescription": car.carDescription,
            "carLicencePhotoUrl": car.carLicencePhotoUrl,
            "carCommentCount": car.carCommentCount,
            "carLikeCount": car.carLikeCount,
            "profile_img_url": account.profile_img_url

        }


        s_car = serializers.serialize('json', [car])

    except AccountManagement.models.Car.DoesNotExist:
        return HttpResponse("Böyle bir araç yok", status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        #return HttpResponse("Kullanıcı girişi yapılmalı",status=status.HTTP_401_UNAUTHORIZED)
        print(e)
        raise e

    return  Response(response, status=status.HTTP_200_OK)

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

    try:
        accont=Account.objects.get(email__exact=email)
    except AccountManagement.models.Account.DoesNotExist:
       return Response({"exist":False},status=status.HTTP_404_NOT_FOUND)

    return Response({"exist":accont.isAcitve},status=status.HTTP_200_OK)

@api_view(["GET"])
def checkUsername(request,username):
    accont=Account.objects.filter(username__exact=username)
    print(accont.__len__())
    response={
        "exist":bool(accont.__len__())
    }
    return Response(response)

@api_view(["POST"])
def addRecentlMessaged(request):

    try:
        decoded = check_access_token(request=request)
        account_uid = decoded['account_uid']
        account=Account.objects.get(account_uid=account_uid)
        target_mail=request.data.get("user_mail")

        target_account=Account.objects.get(email=target_mail)

        account.recently_messaged.add(target_account)
        account.save()




    except AccountManagement.models.Account.DoesNotExist  :
        print("Gecersiz mail adersi")
        return Response("Verediginiz mail adresi bulunamadi",status=status.HTTP_404_NOT_FOUND)

    return Response("Basariyla Eklendi",status=status.HTTP_200_OK)




@api_view(["POST"])
def follow_new_user(request):
    try:
        decoded = check_access_token(request=request)
        account_uid = decoded['account_uid']
        account=Account.objects.get(account_uid=account_uid)
        target_mail=request.data.get("user_mail")

        target_account=Account.objects.get(email=target_mail)

        account.following.add(target_account)
        account.save()




    except AccountManagement.models.Account.DoesNotExist :
        print("Gecersiz mail adersi")
        return Response("Verediginiz mail adresi bulunamadi",status=status.HTTP_404_NOT_FOUND)

    return Response("Basariyla Eklendi",status=status.HTTP_200_OK)



@api_view(["POST"])
def updateUser(request):
    try:
        decoded = check_access_token(request=request)
        account_uid = decoded['account_uid']
        account = Account.objects.get(account_uid=account_uid)


        serializer=AccountUpdateSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            if serializer.validated_data.get('name', False):
                 account.name=serializer.validated_data['name']
            if serializer.validated_data.get('phone', False):
                 account.phone=serializer.validated_data['phone']
            if serializer.validated_data.get('profile_img_url', False):
                 account.profile_img_url=serializer.validated_data['profile_img_url']
            if serializer.validated_data.get('password', False):
                account.password = make_password(serializer.validated_data['password'])



        account.save()



    except Exception as e:
        print(e)
        raise e

    return Response("Basariyla Guncell3endi", status=status.HTTP_200_OK)





@api_view(["GET"])
def getCars(request,email):
    try:
        decoded = check_access_token(request=request)
        account_uid = decoded['account_uid']



        account = Account.objects.get(email__exact=email)
        cars = list(Car.objects.filter(account__exact=account))
        response = []

        for car in cars:
            response.append({

                "carOwnerEmail": car.account.email,
                "carPlate": car.carPlate,
                "carBrand": car.carBrand,
                "carPhotoUrl": car.carPhotoUrl,
                "isCarSale": car.isCarSale,
                "carKm": car.carKm,
                "carDescription": car.carDescription,
                "carLicencePhotoUrl": car.carLicencePhotoUrl,
                "carCommentCount": car.carCommentCount,
                "carLikeCount": car.carLikeCount,
                "postDate":car.postDate,
                "profile_img_url":account.profile_img_url


            })


    except Exception as e:
        print(e)
        raise e

    return Response({"cars": response}, status=status.HTTP_200_OK)


@api_view(["POST"])
def increaseLikeCount(request):
    try:
        decoded = check_access_token(request=request)
        account_uid = decoded['account_uid']





    except Exception as e:
        print(e)
        raise e