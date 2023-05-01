from django.urls import path
from .views import *

urlpatterns = [
    path('', indexView, name="index"),
    path('login/', client_login, name='client_login'),
    path('register/', client_register, name='client_register'),
    path('listing/', carListingView, name='listing'),

]
