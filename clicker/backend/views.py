from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from backend.forms import UserForm
from backend.models import Core, Boost
from backend.serializers import CoreSerializer, BoostSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import viewsets
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
    boosts = Boost.objects.filter(core=core)
    return render(request, 'index.html', {'core': core, 'boosts':boosts})
def user_logout(request):
	logout(request)
	return redirect('login')
@api_view(['GET'])
def call_click(request):
	core = Core.objects.get(user=request.user)
	core.click()
	if core.is_levelup:
		Boost.objects.create(core=core, price=core.level * 10, power=core.level * 5)
	core.save()
	serialized_core = CoreSerializer(core).data
	return Response({'core': serialized_core})
class BoostViewSet(viewsets.ModelViewSet): 
    queryset = Boost.objects.all() 
    serializer_class = BoostSerializer

    def get_queryset(self):
        core = Core.objects.get(user=self.request.user)
        boosts = Boost.objects.filter(core=core)
        return boosts
    def partial_update(self, request, pk):
        boost = self.queryset.get(pk=pk)

        is_levelup = boost.levelup()
        if not is_levelup:
            return Response({ "error": "Не хватает веса" })

        old_boost_stats, new_boost_stats = is_levelup

        return Response({
        "old_boost_stats": self.serializer_class(old_boost_stats).data,
        "new_boost_stats": self.serializer_class(new_boost_stats).data,
    })