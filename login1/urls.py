from django.urls import path

from . import views

urlpatterns = [

    path('index/', views.index),
    path('login/', views.login),
    path('login/', views.register),
    path('logout/', views.logout),
]