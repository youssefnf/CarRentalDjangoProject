from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth import authenticate, login, logout
from .models import *
from datetime import date
from django.core.mail import send_mail

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
                error_login = True
                return render(request, 'login.html', {'form': loginForm, 'error_login': error_login})

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
    all_reservations = Reservation.objects.filter(client=client).order_by('-id')
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

            pending_reservations = Reservation.objects.all().filter(client=client, paye=False)
            num_pending_reservations = len(pending_reservations)
            if num_pending_reservations >= 2 :
                cant_reserve = True
                return render(request, 'addReservation.html', {'car': selectedCar, 'form': form, 'cant_reserve': cant_reserve})

            reservation = Reservation(voiture=selectedCar, client=client, dateDebut=date_debut, dateFin=date_fin, dateReservation=date.today())
            reservation.save()
            successful_res = True
            return render(request, 'addReservation.html', {'car': selectedCar, 'form': form, 'successful_res': successful_res})

    if request.user.is_staff:
        return HttpResponseNotFound("Only Clients cant rent cars!")
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

            if date_debut <= date.today() or date_debut > date_fin:
                print('here')
                dates_not_correct = True
                carAvailability = False
                return render(request, 'addReservation.html', {'car': selectedCar, 'form': form, 'carAvailability': carAvailability, 'datesNotCorrect': dates_not_correct})

            for res in allReservations:
                if not ( (date_debut < res.dateDebut.date() and date_fin < res.dateDebut.date()) or (date_debut > res.dateFin.date() and date_fin > res.dateFin.date())):
                    carAvailability = False
                    date_errors = True

                    
                    print('error de date')
                    return render(request, 'addReservation.html', {'car': selectedCar, 'form': form, 'carAvailability': carAvailability,'carReservations': allReservations , 'date_errors': date_errors})

            
            form = AddReservationForm(request.POST)
            return render(request, 'addReservation.html', {'car': selectedCar, 'form': form, 'carAvailability': carAvailability, 'date_errors': date_errors})

    return redirect('rentCar', carId=carId)

@login_required(login_url='/login')
def manageReservationsView(request):
    all_reservations = Reservation.objects.all().order_by('-id')
    return render(request, 'manageReservations.html', {'reservations': all_reservations})

@login_required(login_url='/login')
def deleteReservationView(request, id):
    if request.user.is_staff or request.user.is_active:
        reservation = get_object_or_404(Reservation, id=id)
        reservation.delete()
        if request.user.is_staff:
            return redirect('manageReservations')
        else:
            return redirect('clientListingReservations')
    else:
        return HttpResponseNotFound("You don't have permission to proceed!")
        

@login_required(login_url='/login')
def confirmReservationView(request, id):
    if request.user.is_staff:
        reservation = get_object_or_404(Reservation, id=id)
        reservation.paye = True
        reservation.save()
        return redirect('manageReservations')
    else:
        return HttpResponseNotFound("You don't have permission to proceed!")
    

def contactUsView(request):
    form = ContactUs()
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        # send_mail(
        #     name + ' have a message',
        #     message,
        #     email,
        #     ['rentcar.django@gmail.com']
        # )

        return render(request, 'contactUs.html', {'name': name, 'form' : form})
    return render(request, 'contactUs.html', {'form': form})


