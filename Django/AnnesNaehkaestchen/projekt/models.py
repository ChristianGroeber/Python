from django.db import models
from froala_editor.fields import FroalaField
import datetime
from django.utils import timezone
# Create your models here.


class Projekt(models.Model):
    titel = models.CharField(max_length=50)
    beschreibung = models.TextField()
    bild = models.ImageField()
    inhalt = FroalaField()
    bild.null = True
    bild.blank = True
    veroeffentlicht = models.DateTimeField('Datum Veröffentlicht')

    def __str__(self):
        return self.titel


class Kommentar(models.Model):
    titel = models.CharField(max_length=50)
    text = models.CharField(max_length=200)

