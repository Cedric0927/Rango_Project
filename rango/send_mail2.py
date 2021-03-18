"""
@Time: 2021/3/5 17:03
@Author: Cedric
"""
import pythoncom
import win32com.client as win32


def send_mail(username, token, mail_type):
    pythoncom.CoInitialize()
    outlook = win32.Dispatch('Outlook.Application')

    mail_item = outlook.CreateItem(0)  # 0: olMailItem

    # mail_item.Recipients.Add('704956727@qq.com')
    mail_item.Recipients.Add(username)
    mail_item.Subject = 'Mail Test'

    mail_item.BodyFormat = 2  # 2: Html format
    name = username.split('.')[0]
    url = 'http://127.0.0.1:8000/rango/{}/?u_token={}'.format(mail_type, token)
    mail_item.HTMLBody = '''
        <h4>Hello {}, </h4>
        <p>Welcome to register Rango, Please click the link to activate your account</p>
        <a href="{}">激活</a>
        <p>If the link can not click, please copy the following link to your browser</p>
        <p>{}</p>
        <p>Best Wishes</p>
        <p>From Cedric</p>
        '''.format(name, url, url)
    mail_item.Send()


if __name__ == '__main__':
    send_mail()
