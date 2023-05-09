from django.urls import path
from . import views



urlpatterns = [
    path('CreateAccount/',views.createAccount),
    path('login/',views.login),
    path('account/',views.getAccount),
    path('newCar/',views.newCar),
    path("confimEmail/<str:token>/",views.emailVerify, name = "emailverify"),
    path('ListmyCars/',views.getMyCars),
    path('newComment/',views.newComment),


    path('carDetails/license=str:<license>',views.CarDetails),

]