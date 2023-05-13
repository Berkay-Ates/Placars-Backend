from rest_framework import serializers
from .models import *
from .models import Account




class AccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Account
        fields=('name','phone','password','profile_img_url')



class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model=Account
        fields=('name','email','phone','password','username','profile_img_url')
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model=Account
        fields=('email','password')

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model=Car
        fields=('license',
                'brand',
                'model',
                'carPhotoLocationNo'
                ,'color'
                ,'satilikMi'
                ,'carKm'
                ,'carLicensePhotoLocationNo')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields = ('content',
                  'title')


















