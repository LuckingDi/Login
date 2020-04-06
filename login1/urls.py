from django.urls import path

from . import views
app_name = 'login1'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout),
]