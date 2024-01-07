from django.contrib import admin as admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]