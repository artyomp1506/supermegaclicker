from django.contrib import admin
from django.urls import path, include
from backend.views import UserLogin, UserRegister, index, user_logout
urlpatterns = [
    path('', index, name='home'),
    path('login',UserLogin.as_view(), name='login'),
    path('logout', user_logout, name='logout'),
    path('register', UserRegister.as_view(), name='register'),
] 
