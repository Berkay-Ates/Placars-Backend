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


    path('carDetails/<str:license>/',views.CarDetails),
    path('checkMail/<str:email>/',views.checkMail),
    path('checkUsername/<str:username>/', views.checkUsername),
    path('add_recently_messaged/', views.addRecentlMessaged),
    path('follow_new_user/', views.follow_new_user),

]