from django.urls import path
from . import views



urlpatterns = [
    path('CreateAccount/',views.createAccount),
    path('login/',views.login)


]