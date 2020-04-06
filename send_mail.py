import os
from django.core.mail import send_mail, EmailMultiAlternatives

os.environ['DJANGO_SETTINGS_MODULE'] = 'Login.settings'

if __name__ == '__main__':

    # send_mail(
    #     'Django 测试邮件',                                  # 主题
    #     'hahada@aliyun.com作为测试邮箱的测试邮件',             # 邮件内容
    #     'hahada@aliyun.com',                                # 邮件发送方
    #     ['hahada@aliyun.com'],                              # 接收方邮箱列表
    # )

    subject, from_email, to = '来自Django的测试邮件', 'hahada@aliyun.com', '836068002@qq.com'
    text_content = '欢迎访问www.baidu.com，这里是刘江的博客和教程站点，专注于Python和Django技术的分享！'
    html_content = '<p>欢迎访问<a href="www.baidu.com" target=blank>www.baidu.com</a>，这里是刘江的博客和教程站点，本站专注于Python、Django和机器学习技术的分享！</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()