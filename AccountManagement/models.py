from django.db import models
from uuid import uuid4


# Create your models here.
class Account(models.Model):
    account_uid = models.UUIDField(default=uuid4, editable=False, unique=True, db_index=True)
    name = models.CharField(max_length=30, blank=False, null=True)
    password = models.CharField(max_length=256 ,blank=False, null=True)
    username=models.CharField(max_length=256)
    email = models.EmailField(blank=False, null=True)
    userIp = models.GenericIPAddressField(unpack_ipv4=True, blank=True, null=True)
    latitude = models.CharField(max_length=10, blank=True, null=True)
    longitude = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    createDate = models.DateTimeField(auto_now_add=True)
    isAcitve=models.BooleanField(default=False)
    following=models.ManyToManyField('self',default=None,null=True,blank=True,symmetrical=False,related_name='following_list')
    profile_img_url=models.CharField(max_length=256,default=None,null=True,blank=True)
    recently_messaged=models.ManyToManyField('self',default=None,null=True,blank=True,symmetrical=False,related_name='message_list')


    def __str__(self):
        return f"{self.email}"







class Car(models.Model):
    account = models.ForeignKey(Account,on_delete=models.CASCADE, blank=True, null=True)
    car_uid = models.UUIDField(primary_key=True,default=uuid4, editable=False, unique=True, db_index=True)
    carPlate = models.CharField(max_length=9, blank=False, null=False)
    carBrand = models.CharField(max_length=30, blank=True, null=True)
    carPhotoUrl = models.CharField(max_length=256, blank=True, null=True)
    postDate = models.DateTimeField(auto_now_add=True)
    isCarSale=models.BooleanField(default=False)
    carKm=models.IntegerField(default=0)
    carDescription=models.CharField(max_length=500, blank=True, null=True)
    carLicencePhotoUrl=models.CharField(max_length=256, blank=True, null=True)
    carCommentCount=models.IntegerField(default=0)
    carLikeCount=models.IntegerField(default=0)



    def __str__(self):
        return f"{self.carBrand} "

class Comment(models.Model):
    comment_uid = models.UUIDField(primary_key=True,default=uuid4, editable=False, unique=True, db_index=True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="comments_authored",null=True,blank=True)
    targetCar = models.ForeignKey(Car, on_delete=models.CASCADE,related_name="comments_targetCar", to_field='car_uid')
    createDate = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    content = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.title



class AccountSession(models.Model):
    account_uid = models.UUIDField(primary_key=True,default=uuid4, editable=False, unique=True, db_index=True)
    name = models.CharField(max_length=30, blank=False, null=True)
    userIp = models.GenericIPAddressField(unpack_ipv4=True, blank=True, null=True)
    latitude = models.CharField(max_length=10, blank=True, null=True)
    longitude = models.CharField(max_length=10, blank=True, null=True)
    createDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

