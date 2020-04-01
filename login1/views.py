from django.shortcuts import render, redirect
from . import models, forms


def index(request):
    if not request.session.get('is_login', None):
        return redirect('/login1/login/')
    return render(request, 'login1/index.html')


def login(request):
    if request.session.get('is_login', None):       # 不允许重复登录
        return redirect('/login1/index/')
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = '请检查填写内容'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            try:
                user = models.User.objects.get(name=username)
            except:
                message = '用户名或密码有误。'
                return render(request, 'login1/login.html', locals())
            if user.password == password:
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/login1/index/')
            else:
                message = '用户名或密码有误。'
                return render(request, 'login1/login.html', locals())
        else:
            message = '用户名或密码不能为空'
            return render(request, 'login1/login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'login1/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect('/login1/login/')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "请检查输入内容"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')

    return render(request, 'login1/register.html')


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/login1/login/')
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect('/login1/login/')
