from django.urls import path

from . import views

urlpatterns = [

    path('index/', views.index),
    path('login1/', views.login),
    path('register/', views.register),
    path('logout/', views.logout),
]