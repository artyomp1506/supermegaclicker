from django.contrib import admin
from django.urls import path, include
from backend.views import index,user_login,user_logout,register
urlpatterns = [
    path('', index, name='home'),
    path('login', user_login, name='login'),
    path('logout', user_logout, name='logout'),
    path('register', register, name='register'),
] 
