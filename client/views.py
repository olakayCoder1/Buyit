from django.http import HttpResponse
from django.shortcuts import render
from account.models import User
from .models import *
from django.contrib.auth import authenticate, login ,logout
# Create your views here.



def home_page(request):

    if request.method == 'POST' :
        email = request.POST['username']
        password = request.POST['password']

        user = authenticate(email=email, password=password)
        if user is not None :
            login(request,user)
            return HttpResponse('YOU ARE LOGGGED IN')
    # print(user.owner.all()) 
    return render(request, 'client/home.html')