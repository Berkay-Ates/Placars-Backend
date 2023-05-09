from rest_framework import serializers
from .models import Account,Car,Comment

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model=Account
        fields=('name','email','phone','password','username')
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model=Account
        fields=('email','password')

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model=Car
        fields=('license','brand','model','carPhotoLocationNo','color','satilikMi','carKm','carLicensePhotoLocationNo')



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=('author','targetCar','model','content','title')


