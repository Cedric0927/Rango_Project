"""
@Time: 2021/3/15 15:05
@Author: Cedric
"""
from Rango_Project import settings
from django.core.mail import send_mail


def send_verify_email(to_email='704956727@qq.com', verify_url=1):
    """
    发送验证邮箱邮件
    :param to_email: 收件人地址
    :param verify_url:验证链接
    :return:None
    """
    subject = "邮箱验证"
    html_message = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用Rango。</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="%s">%s<a></p>' % (to_email, verify_url, verify_url)
    send_mail(subject, "", 'Cedric.Niu@rosenbergerap.com', [to_email], html_message=html_message)


if __name__ == '__main__':
    send_verify_email()