from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout, login, authenticate
from backend.forms import UserForm
def index(request):
	return render(request,'index.html')
def register(request):
	if request.method=='POST':
		form=UserForm(request.POST)
		if form.is_valid():
			user=form.save()
			login(request,user)
			return redirect('home')
		return render(request, 'register.html', {'form': form, 'user':request.user})
	form=UserForm()
	return render(request, 'register.html', {'form': form, 'user':request.user})	
def user_login(request):
	form=UserForm()
	if request.method=='POST':
		user=authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
		if user:
			login(request,user)
			return redirect('home')
		return render(request, 'login.html', {'form': form, 'user':request.user, 'invalid':True})	
	return render(request, 'login.html', {'form': form, 'user':request.user, 'invalid':False})
def user_logout(request):
	logout(request)
	return redirect('login')
