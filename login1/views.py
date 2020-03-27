from django.shortcuts import render, redirect


def index(request):
    pass
    return render(request, 'login1/1.html')


def login(request):
    pass
    return render(request, 'login1/login.html')


def register(request):
    pass
    return render(request, 'login1/register.html')


def logout(request):
    pass
    return redirect('/login/')
