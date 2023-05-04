from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Voiture)
class VoitureModelAdmin(admin.ModelAdmin):
    pass

@admin.register(Client)
class ClientModelAdmin(admin.ModelAdmin):
    pass

@admin.register(Reservation)
class ReservationModelAdmin(admin.ModelAdmin):
    pass