from django.shortcuts import render, redirect


def index(request):
    pass
    return render(request, 'login1/index.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        return redirect('/index/')
    return render(request, 'login1/1.html')


def register(request):
    pass
    return render(request, 'login1/register.html')


def logout(request):
    pass
    return redirect('/login/')
