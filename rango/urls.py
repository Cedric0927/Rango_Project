"""
@Author: Cedric
@Time: 2021.03,09
"""
from django.urls import path

from rango import views

urlpatterns = [
    path('', views.index, name='index')
]