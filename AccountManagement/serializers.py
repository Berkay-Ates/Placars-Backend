from rest_framework import serializers
from .models import Account,Car

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model=Account
        fields=('name','email','phone','password')

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model=Car
        fields=('license','brand','model','carPhotoLocationNo','color')