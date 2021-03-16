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
    path('bootstrap_login/', views.bootstrap_login, name='bootstrap_login')

]
