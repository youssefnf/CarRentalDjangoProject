from django.shortcuts import render, HttpResponse
from .forms import LoginForm

# Create your views here.

def indexView(request):
    return render(request, 'index.html')


def client_login(request):
    if request.method == 'POST':
        pass
    else:
        loginForm = LoginForm()
        return render(request, 'login.html', {'form': loginForm})

