from django.db import models
import datetime
from django.utils import timezone
# Create your models here.


class Projekt(models.Model):
    titel = models.CharField(max_length=50)
    beschreibung = models.TextField()
    bild = models.ImageField()
    bild.null = True
    bild.blank = True
    veroeffentlicht = models.DateTimeField('Datum Veröffentlicht')

    def __str__(self):
        return self.titel

