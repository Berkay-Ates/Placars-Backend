from django.db import models
from uuid import uuid4


# Create your models here.
class Account(models.Model):
    account_uid = models.UUIDField(default=uuid4, editable=False, unique=True, db_index=True)
    name = models.CharField(max_length=30, blank=False, null=True)
    password = models.CharField(max_length=256 ,blank=False, null=True)
    username=models.CharField(max_length=256,blank=False,null=False)
    email = models.EmailField(blank=False, null=True)
    userIp = models.GenericIPAddressField(unpack_ipv4=True, blank=True, null=True)
    latitude = models.CharField(max_length=10, blank=True, null=True)
    longitude = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    createDate = models.DateTimeField(auto_now_add=True)
    isAcitve=models.BooleanField(default=False)
    following=models.ManyToManyField('self',default=None)




    def __str__(self):
        return f"{self.name}"





class AccountSession(models.Model):
    account_uid = models.UUIDField(primary_key=True,default=uuid4, editable=False, unique=True, db_index=True)
    name = models.CharField(max_length=30, blank=False, null=True)
    userIp = models.GenericIPAddressField(unpack_ipv4=True, blank=True, null=True)
    latitude = models.CharField(max_length=10, blank=True, null=True)
    longitude = models.CharField(max_length=10, blank=True, null=True)
    createDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"


class Car(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    car_uid = models.UUIDField(primary_key=True,default=uuid4, editable=False, unique=True, db_index=True)
    license = models.CharField(max_length=9, blank=False, null=False)
    brand = models.CharField(max_length=30, blank=True, null=True)
    model = models.CharField(max_length=40, blank=True, null=True)
    carPhotoLocationNo = models.CharField(max_length=100, blank=True, null=True)
    carLicensePhotoLocationNo = models.CharField(max_length=100, blank=True, null=True)

    color = models.CharField(max_length=10, blank=True, null=True)
    createDate = models.DateTimeField(auto_now_add=True)
    satilikMi=models.BooleanField(default=False)
    carKm=models.IntegerField()



    def __str__(self):
        return f"{self.model} {self.brand} "


class Comment(models.Model):
    comment_uid = models.UUIDField(primary_key=True,default=uuid4, editable=False, unique=True, db_index=True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="comments_authored")
    targetCar = models.ForeignKey(Car, on_delete=models.CASCADE)
    createDate = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    commentReceiver = models.ForeignKey(
        Account, on_delete=models.CASCADE, blank=True, null=True, related_name="comments_received"
    )
    content = models.CharField(max_length=100, blank=False, null=False)
    title = models.CharField(max_length=30, blank=False, null=False)

    def __str__(self):
        return self.title
