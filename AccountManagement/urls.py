from django.urls import path
from . import views



urlpatterns = [
    path('CreateAccount/',views.createAccount),
    path('login/',views.login),
    path('account/',views.getAccount),
    path('newCar/',views.newCar)


]