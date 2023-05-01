from django.urls import path
from .views import *

urlpatterns = [
    path('', indexView, name="index"),
    path('login/', client_login, name='client_login'),
    path('listing/', carListingView, name='listing'),

]
