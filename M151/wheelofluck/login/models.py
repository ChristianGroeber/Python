from django.db import models
from django.db.models import ForeignKey
from django.utils import timezone
from datetime import datetime
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


class Answer(models.Model):
    text = models.CharField(max_length=200, default="")
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


def get_random_word():
    words = Word.objects.all()
    return random.choice(words)


class Word(models.Model):
    word = models.CharField(max_length=50)
    category = ForeignKey(Category, on_delete=models.CASCADE)
    consonants = []
    guessed = []
    answer = models.ManyToManyField(Answer)

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
        if not self.consonants:
            self. fill_consonants(self)
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
    word = models.CharField(max_length=100)
    # assigned_to_player = ForeignKey(Player, on_delete=models.CASCADE)
    found_consonants = []
    # consonants = word.words.all()

    def __str__(self):
        return self.word

    def add_found_consonant(self, string):
        self.found_consonants[len(self.found_consonants)] = string


class Game(models.Model):
    @property
    def amount_played(self):
        return self._amount_played

    player = models.CharField(max_length=30)
    date_played = models.DateTimeField('Date Played')
    amount_played = models.IntegerField(default=0)
    konsonant = models.CharField(max_length=1)
    wort = ForeignKey(Word, default=1, on_delete=models.CASCADE)
    output = models.CharField(max_length=200, default="")
    found_consonants = []
    built_word = ""
    test = models.CharField(max_length=50, default=0)
    spielrunden = models.CharField(max_length=20, default=0)

    def __str__(self):
        return self.player + " - " + str(self.amount_played) + " - " + str(self.date_played.strftime("%d.%m.%Y")) + \
               " - " + str(self.spielrunden)

    def set_amount(self, amount):
        self.amount_played = amount

    def set_player(self):
        self.player = Player.objects.get(pk=self.player_id).player_name

    @classmethod
    def create(cls, player):
        sel_word = get_random_word()
        arr = sel_word.word.split()
        output = ""
        for x in arr:
            for i in range(0, len(x)):
                output += "_ "
            output += "- "
        return cls(player=player, date_played=timezone.now(), wort=sel_word, output=output)

    def generate_output(self, consonant_to_putin):
        if not self.built_word:
            self.built_word = self.output
        print('amount of occurances: ' + str(self.wort.word.count(consonant_to_putin)))
        found = 1
        temp = self.built_word
        self.built_word = ""
        arr = list(str(self.wort))
        print('arr: ' + str(arr))
        x = 0
        for y2 in arr:
            if any(y2 in s for s in self.found_consonants):
                self.built_word += y2
            elif y2.isspace():
                self.built_word += "-\n"
            elif not temp.split()[x] == "_\n":
                self.built_word += temp.split()[x]
            else:
                self.built_word += "_ "
            x = x + 1
        print('output: ' + self.built_word)
        return self.built_word

    def get_amount_played(self):
        return self._amount_played + 0
