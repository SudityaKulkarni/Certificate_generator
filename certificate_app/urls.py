from django.contrib import admin
from django.urls import path

from .views import generate_certificate

urlpatterns = [
    path('generate_certificate/',generate_certificate,name='certificate generation')
]