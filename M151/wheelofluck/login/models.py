from django.db import models
from django.db.models import ForeignKey
import random

# Create your models here.exit


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
    consonants = []
    guessed = []

    def fill_consonants(self):
        consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x',
                      'y', 'z']
        splitted_word = self.word.split()
        for string in splitted_word:
            if any(string in s for s in consonants):
                self.consonants[len(self.consonants)] = string
        print(self.consonants)

    def __str__(self):
        return self.word

    def guess_consonant(self, string):
        if any(string in s for s in self.consonants):
            self.guessed[len(self.guessed)] = string
            return True
        else:
            return False


# There's a new Player for each game
class Player(models.Model):
    player_name = models.CharField(max_length=30)


# The word a Player has to guess in a game
class PlayerWord(models.Model):
    word = ForeignKey(Word, related_name='words', on_delete=models.CASCADE)
    assigned_to_player = ForeignKey(Player, on_delete=models.CASCADE)
    found_consonants = []
    # consonants = word.words.all()

    def __str__(self):
        return self.word

    def add_found_consonant(self, string):
        self.found_consonants[len(self.found_consonants)] = string


class Game(models.Model):
    player = models.CharField(max_length=30)
    date_played = models.DateTimeField('Date Played')
    amount_played = models.IntegerField(default=0, editable=False)
    konsonant = models.CharField(max_length=1)

    def __str__(self):
        return self.player

    def set_amount(self, amount):
        self.amount_played = amount

    def set_player(self):
        self.player = Player.objects.get(pk=self.player_id).player_name

    # gets all the words then returns the value "word" of a random one.
    @staticmethod
    def get_random_word():
        words = Word.objects.get(all)
        sel_word = random.choice(words).word
        print(sel_word)
        return sel_word

