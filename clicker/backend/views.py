from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from backend.forms import UserForm
from backend.models import Core
from backend.serializers import CoreSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
class UserRegister(APIView):
    def get(self, request):
        form = UserForm()
        return render(request, 'register.html', {'form': form})
    def post(self, request):
        form = UserForm(request.POST) 
        if form.is_valid(): 
            user = form.save() 
            login(request, user)

            user_core = Core(user=user)
            user_core.save()
            return redirect('home')

        return render(request, 'register.html', {'form': form})

class UserLogin(APIView):
    form = UserForm()
    def get(self, request):
        return render(request, 'login.html', {'form': self.form})

    def post(self, request):
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password')) 
        if user!=None:
            login(request, user) 
            return redirect('home')
        return render(request, 'login.html', {'form': self.form, 'invalid': True})
   
@login_required
def index(request):         
    core = Core.objects.get(user=request.user)
    return render(request, 'index.html', {'core': core})
def user_logout(request):
	logout(request)
	return redirect('login')
@api_view(['GET'])
def call_click(request):
	core=Core.objects.get(user=request.user)
	core.click()
	core.save()
	serialized_core = CoreSerializer(core).data
	print(dir(serialized_core))
	return Response({ 'core': serialized_core })
