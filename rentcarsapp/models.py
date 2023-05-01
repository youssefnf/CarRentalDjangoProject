from django.db import models

# Create your models here.

class Voiture(models.Model):
    matricule = models.CharField(max_length=10)
    marque = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    prix = models.FloatField()
