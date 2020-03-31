from django.shortcuts import render, redirect
from . import models


def index(request):
    pass
    return render(request, 'login1/index.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username.strip() and password:
            try:
                user = models.User.objects.get(name=username)
            except:
                message = '用户名或密码有误。'
                return render(request, 'login1/login.html', {'message': message})
            if user.password == password:
                return redirect('/login1/index/')
            else:
                message = '用户名或密码有误。'
                return render(request, 'login1/login.html', {'message': message})
        else:
            message = '用户名或密码不能为空'
            return render(request, 'login1/login.html', {'message': message})
    else:
        return render(request, 'login1/login.html')


def register(request):
    pass
    return render(request, 'login1/register.html')


def logout(request):
    pass
    return redirect('/login1/')
