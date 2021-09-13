from django.contrib import admin
from django.urls import path

from .views import contactView, successView

app_name='contact'

urlpatterns = [
    path('contactus/', contactView, name='contactus'),
    path('success/', successView, name='success'),
]