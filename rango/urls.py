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
]