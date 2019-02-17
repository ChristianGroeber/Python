from django.db import models

# Create your models here.exit
from django.db.models import ForeignKey


class UserLogin(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    loggedInAt = models.DateTimeField('Date Published')

    def __str__(self):
        return self.username


class Category(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category

    def arr_from_cats(self):
        self.Objects.all()


class Word(models.Model):
    word = models.CharField(max_length=50)
    category = ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.word


class Game(models.Model):
    player = models.CharField(max_length=30)
    date_played = models.DateTimeField('Date Played')
    amount_played = models.IntegerField()

    def __str__(self):
        return self.player

