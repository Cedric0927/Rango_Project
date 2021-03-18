"""
@Author: Cedric
@Time: 2021.03,09
"""
from django.urls import path

from rango import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_category/', views.add_category, name="add_category"),
    path('<slug>', views.show_category, name="show_category"),
    path('add_page/<category_slug>', views.add_page, name="add_page"),
    path('register/', views.register, name="register"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('bootstrap_register/', views.bootstrap_register, name='bootstrap_register'),
    path('bootstrap_login/', views.bootstrap_login, name='bootstrap_login'),
    path('register3/', views.register3, name='register3'),
    path('login3/', views.login3, name='login3'),
    path('sendmail/', views.send_email, name="sendmail"),
    path('activate/', views.activate, name='activate'),
    path('change_password/', views.change_password, name='change_password'),
    path('setcookie/', views.set_cookie, name='setcookie'),
    path('getcookie/', views.get_cookie, name='getcookie'),
    path('forget/', views.forget_password, name='forget_password'),
    path('send_mail/', views.send_email, name='send_email'),
    path('test/', views.test, name='test'),
]
