from django.db import models
from django.contrib.auth.models import User

CARBURANT_CHOICES = (
    ('essance', 'ESSENCE'),
    ('diesel', 'DIESEL'),
)

# Create your models here.

class Voiture(models.Model):
    matricule = models.CharField(max_length=10)
    marque = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    prix = models.FloatField()
    nb_portes = models.PositiveBigIntegerField(default=0)
    nb_passager = models.PositiveBigIntegerField(default=0)
    carburant = models.CharField(max_length=10, choices=CARBURANT_CHOICES, default='diesel')
    image = models.ImageField(null=True, blank=False, upload_to="images/")
    
    def __str__(self):
        return f"{self.marque} {self.model}"
    

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=20)
    prenom = models.CharField(max_length=20)
    telephone = models.CharField(max_length=12)
    email = models.CharField(max_length=50)
    dateCreation = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        return f"{self.nom} {self.prenom}"

class Reservation(models.Model):
    voiture = models.ForeignKey(Voiture, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    dateDebut =  models.DateTimeField()
    datefin =  models.DateTimeField()
    dateReservation = models.DateField(null=True)

    def __str__(self):
        return f"{self.voiture} {self.client}"

