from django.shortcuts import render, redirect
from . import models, forms


def index(request):
    if not request.session.get('is_login', None):
        return redirect('/login1/login/')
    return render(request, 'login1/index.html')


def login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
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
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/login1/index/')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "请检查输入内容。。。"

        # if register_form.is_valid():
        # username = register_form.cleaned_data.get('username1')
        # password1 = register_form.cleaned_data.get('password1')
        # password2 = register_form.cleaned_data.get('password2')
        # email = register_form.cleaned_data.get('email')
        # sex = register_form.cleaned_data.get('sex')

        username = request.POST.get('username1', 'USERNAME')
        password1 = request.POST.get('password1', 'PASSWORD1')
        password2 = request.POST.get('password2', 'PASSWORD2')
        email = request.POST.get('email', 'EMAIL')
        sex = request.POST.get('sex', 'SEX')

        if password1 != password2:
            message = '两次密码不同，请重新输入！'
            return render(request, 'login1/register.html', locals())
        else:
            same_name_user = models.User.objects.filter(name=username)
            if same_name_user:
                message = '用户名已存在，请重新输入。'
                return render(request, 'login1/register.html', locals())
            a = "@"
            b = ".com"
            if a in email and b in email:
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '邮箱已存在，请重新输入。'
                    return render(request, 'login1/register.html', locals())

                new_user = models.User()
                new_user.name = username
                new_user.password = password1
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                code = make_
                message = '注册成功！请登录。'
                return render(request, 'login1/login.html', locals())
            else:
                message = '输入的邮箱格式有误，请重新输入'
                return render(request, 'login1/register.html', locals())
    # else:
    #     return render(request, 'login1/register.html', locals())

    else:
        return render(request, 'login1/register.html', )


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/login1/login/')
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect('/login1/login/')
