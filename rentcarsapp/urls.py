from django.urls import path
from .views import *

urlpatterns = [
    path('', indexView, name="index"),
    path('login/', loginView, name='login'),
    path('logout/', logoutView, name='logout'),
    path('register/', registerView, name='register'),
    path('listing/', carListingView, name='listing'),
    path('listing/filter/', carListingFilterView, name='listing-filter'),
    path('clientListingReservations/', clientReservationListingView, name='clientListingReservations'),
    path('rentCar/<int:carId>', rentCarView, name='rentCar'),
    path('checkAvailability/<int:carId>', checkCarAvailabilityView, name='checkavailability'),
    path('manageReservations/', manageReservationsView, name="manageReservations"),
    path('confirmReservation/<int:id>', confirmReservationView, name='confirmReservation'),
    path('deleteReservation/<int:id>', deleteReservationView, name="deleteReservation"),

]
