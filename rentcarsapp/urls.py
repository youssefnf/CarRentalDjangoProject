from django.urls import path
from .views import *

urlpatterns = [
    path('', indexView, name="index"),
    path('login/', loginView, name='login'),
    path('logout/', logoutView, name='logout'),
    path('register/', registerView, name='register'),
    path('listing/', carListingView, name='listing'),
    path('listing/filter/', carListingFilterView, name='listing-filter'),
    path('listingReservations/', reservationListingView, name='listingReservations'),

]
