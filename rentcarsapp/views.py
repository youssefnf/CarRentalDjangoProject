from django.shortcuts import render, HttpResponse
from .forms import LoginForm
from .models import *

# Create your views here.

def indexView(request):
    return render(request, 'index.html')


def client_login(request):
    if request.method == 'POST':
        pass
    else:
        loginForm = LoginForm()
        return render(request, 'login.html', {'form': loginForm})
    

def carListingView(request):
    all_cars = Voiture.objects.all()
    return render(request, 'carListing.html', {'cars': all_cars})

