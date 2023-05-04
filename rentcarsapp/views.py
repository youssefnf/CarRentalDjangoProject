from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth import authenticate, login, logout
from .models import *
from datetime import date

# Create your views here.

def indexView(request):
    try:
        connected_client = get_object_or_404(Client, user=request.user)
    except:
        return render(request, 'index.html')
    
    return render(request, 'index.html', {'client': connected_client})


def loginView(request):
    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            loginData = loginForm.cleaned_data
            user = authenticate(request, username=loginData['username'], password=loginData['password'])

            if user is not None:
                login(request, user)
                return redirect('index')

    else:
        loginForm = LoginForm()
        return render(request, 'login.html', {'form': loginForm})

def logoutView(request):
    logout(request)
    return redirect('index')
    
def registerView(request):
    if request.method == 'POST':
        registerForm = CustomUserCreationFrom(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.save()

            client = Client()
            client.user = user
            client.nom = user.last_name
            client.prenom = user.first_name
            client.email = user.email
            client.save()
            
            user = authenticate(request, username=user.username, password=request.POST['password1'])
            if user is not None:
                login(request, user)
                return redirect('index')

    registerForm = CustomUserCreationFrom()
    return render(request, 'register.html', {'form': registerForm})
    

def carListingView(request):
    all_cars = Voiture.objects.all()
    marques = []
    for car in all_cars:
        marques.append(car.marque)
    marques = list(dict.fromkeys(marques))
    return render(request, 'carListing.html', {'cars': all_cars, 'marques': marques})


def carListingFilterView(request):
    all_cars = Voiture.objects.all()
    marque = request.GET.get('marque')
    all_cars = all_cars.filter(marque=marque)
    return render(request, 'carListing.html', {'cars': all_cars})


def clientReservationListingView(request):
    client = get_object_or_404(Client, user=request.user)
    all_reservations = Reservation.objects.filter(client=client)
    return render(request, 'reservationsListing.html', {'reservations': all_reservations})

@login_required(login_url='/login')
def rentCarView(request, carId):
    if request.method == 'POST':
        form = AddReservationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            date_debut = data["date_debut"].date()
            date_fin = data["date_fin"].date()
            selectedCar = get_object_or_404(Voiture, id=carId)
            client = get_object_or_404(Client, user=request.user)
            reservation = Reservation(voiture=selectedCar, client=client, dateDebut=date_debut, dateFin=date_fin, dateReservation=date.today())
            reservation.save()
            successful_res = True
            return render(request, 'addReservation.html', {'car': selectedCar, 'form': form, 'successful_res': successful_res})

    selectedCar = get_object_or_404(Voiture, id=carId)
    form = AddReservationForm()
    carAvailability = False
    return render(request, 'addReservation.html', {'car': selectedCar, 'form': form, 'carAvailability': carAvailability})


def checkCarAvailabilityView(request, carId):
    if(request.POST):
        form = AddReservationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            date_debut = data["date_debut"].date()
            date_fin = data["date_fin"].date()
            selectedCar = get_object_or_404(Voiture, id=carId)
            allReservations = Reservation.objects.filter(voiture=selectedCar)
            carAvailability = True
            date_errors = False
            print(allReservations)
            for res in allReservations:
                if not ( (date_debut < res.dateDebut.date() and date_fin < res.dateDebut.date()) or (date_debut > res.datefin.date() and date_fin > res.datefin.date())):
                    carAvailability = False
                    date_errors = True
                    
                    print('error de date')
                    return render(request, 'addReservation.html', {'car': selectedCar, 'form': form, 'carAvailability': carAvailability, 'date_errors': date_errors})

            
            form = AddReservationForm(request.POST)
            return render(request, 'addReservation.html', {'car': selectedCar, 'form': form, 'carAvailability': carAvailability, 'date_errors': date_errors})

    return redirect('rentCar', carId=carId)