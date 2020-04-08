from django.shortcuts import render, redirect
from django.conf import settings
from . import models, forms, make_code_string
from django.core.mail import EmailMultiAlternatives
import datetime


def send_email(code, email):

    subject = "来自哈哈哒的注册确认邮件"            # 主题

    text_content = '''
                    感谢注册哈哈哒，这是哈哈哒站点.     
                   如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''    # text文本内容

    html_content = '''
                    <p>感谢注册<a href="http://{}/login1/confirm/?code={}" target=blank>www.hahada.com</a>，
                    这里是刘江的博客和教程站点，专注于Python、Django和机器学习技术的分享！</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)   # html格式内容

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    print(settings.EMAIL_HOST_USER + '-->' + email)
    msg.send()


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

            if not user.has_confirmed:
                message = '该用户尚未进行邮箱验证'
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

                code = make_code_string.make_code(new_user)
                send_email(code, email)

                message = '注册成功！请登录。'
                return render(request, 'login1/login.html', locals())
            else:
                message = '输入的邮箱格式有误，请重新输入'
                return render(request, 'login1/register.html', locals())
    # else:
    #     return render(request, 'login1/register.html', locals())

    else:
        return render(request, 'login1/register.html', )


# 登出
def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/login1/login/')
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect('/login1/login/')


# 注册邮件确认
def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.confirmString.objects.get(code=code)
    except:
        message = "无效的验证码"
        return render(request, 'login1/confirm.html', message)

    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):    # 验证注册时间加上settings中有效时间是否小于现在的时间
        confirm.user.delete()       # 删除此用户以及验证码
        message = "您的邮件注册码已经过期，请重新注册。"
        return render(request, 'login1/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True       # 修改user表中has_confirmed的值
        confirm.user.save()                     # 保存user表
        confirm.delete()                        # 删除confirm表中的code的值
        message ="尊敬的" + confirm.user.name + "，感谢确认，请使用账户登陆！"
        return render(request, 'login1/confirm.html', locals())

