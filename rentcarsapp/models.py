from django.db import models

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
