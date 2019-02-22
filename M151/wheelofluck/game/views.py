import random

from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import NewGame
from .models import Game, Word

# Create your views here.


def index(request):
    print(request)
    return render(request, 'game/index.html')


def game(request):
    print(request)
    if request.method == "POST":
        form = NewGame(request.POST)
        if form.is_valid():
            gm = form.save(commit=False)
            gm.date_played = timezone.now()
            gm.save()
            # question = Game.get_random_word()
            return redirect('betrag')
    else:
        form = NewGame
        return render(request, 'game/game.html', {'form': form})


def spin_wheel(request):
    vals = ['10', '25', '50', '100', '500', 'x2', 'x4', 'Aussetzen', 'Bankrott']
    spinned = random.choice(vals)
    print(spinned)
    return render(request, 'game/betrag.html')
