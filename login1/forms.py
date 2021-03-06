from django import forms
from captcha.fields import CaptchaField


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128)
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput)
    captcha = CaptchaField(label="验证码")


class RegisterForm(forms.Form):
    gender = (
        ('male', '男'),
        ('female', '女'),
    )
    username = forms.CharField(label="用户名", max_length=128, )
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput)
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput)
    email = forms.EmailField(label="邮箱地址")
    sex = forms.CharField(label='性别',)
    # captcha = CaptchaField(label="验证码")

