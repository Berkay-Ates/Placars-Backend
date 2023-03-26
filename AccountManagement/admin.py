from django.contrib import admin
from .models import Account,Car,Comment,AccountSession
# Register your models here.

admin.site.register(Account)
admin.site.register(Car)
admin.site.register(Comment)
admin.site.register(AccountSession)


