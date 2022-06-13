from django.contrib import admin
from django.urls import path, include
from backend.views import UserLogin, UserRegister, index, user_logout, call_click, BoostViewSet
particulal_boost = BoostViewSet.as_view({
    'put': 'partial_update',
})
urlpatterns = [
    path('', index, name='home'),
    path('login',UserLogin.as_view(), name='login'),
    path('logout', user_logout, name='logout'),
    path('register', UserRegister.as_view(), name='register'),
    path('call_click', call_click, name='call_click'),
    path('boost/<int:pk>/', particulal_boost, name='boost')
] 
