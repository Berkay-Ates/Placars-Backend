from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Account,AccountSession,Car
from .serializers import AccountSerializer,CarSerializer
import requests
from django.contrib.auth.hashers import make_password , check_password
from .utils import generate_access_token,check_access_token
from django.core import serializers



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
                                userIp=get_ip(request),phone=serializer.validated_data.get('phone', None),
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
    try:

        serializer=AccountSerializer(data=request.data) # gonderilen istekteki gelen verinin uygun olup olmadigi kontrol ediliyork
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
            instance=Account.objects.get(account_uid=account_uid)
            print("decoded ne ",decoded)
            account={
                "name":instance.name,
                "email":instance.email
            }
                
            return Response(account,status.HTTP_200_OK)

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
                instance=Car.objects.get(license=serializer.validated_data["license"])            
            except Car.DoesNotExist:

                instance=Car(account_uid=account_uid, license=serializer.validated_data["license"],
                             brand=serializer.validated_data.get('brand', None),model=serializer.validated_data.get('model', None),
                             carPhotoLocationNo=serializer.validated_data.get('carPhotoLocationNo', None),
                             color=serializer.validated_data.get('color', None))
                
                

            return Response("Yeni arac olusturuldu", status=status.HTTP_201_CREATED)

        else:
            print('serializer valid degil')
            return Response('Bad Request',status=status.HTTP_400_BAD_REQUEST)





        




        
    except Exception as e:
        print(e)
        raise e

    












