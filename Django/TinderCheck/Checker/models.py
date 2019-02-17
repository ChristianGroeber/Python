from builtins import int, property

from django.db import models

# Create your models here.


class Check(models.Model):
    name = models.CharField(max_length=200)
    age = models.CharField(max_length=2)
    love_for_beer = models.IntegerField(max_length=10)

    @property
    def check_if_match(self):
        highestNumber = 2, 147, 483, 647
        return self.love_for_beer / 2 < highestNumber

    def __str__(self):
        return self.name

