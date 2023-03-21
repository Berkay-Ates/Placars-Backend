from django.contrib import admin
from .models import Account,Car,Comment
# Register your models here.

admin.site.register(Account)
admin.site.register(Car)
admin.site.register(Comment)