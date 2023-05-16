from django.urls import path
from . import views



urlpatterns = [
    path('CreateAccount/',views.createAccount),
    path('login/',views.login),
    path('view_account/',views.view_account),
    path('newCar/',views.newCar),
    path('deleteCar/', views.deleteCar),
    path("confimEmail/<str:token>/",views.emailVerify, name = "emailverify"),
    path('ListmyCars/',views.getMyCars),
    path('ListCars/<str:email>/',views.getCars),
    path('newComment/',views.newComment),
    path('increaseLikeCount/',views.increaseLikeCount),


    path('carDetails/<str:carPlate>/',views.CarDetails),
    path('checkMail/<str:email>/',views.checkMail),
    path('checkUsername/<str:username>/', views.checkUsername),
    path('add_recently_messaged/', views.addRecentlMessaged),
    path('follow_new_user/', views.follow_new_user),
    path('updateUser/', views.updateUser),

]