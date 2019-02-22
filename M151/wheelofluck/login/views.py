import random

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.utils import timezone
from django_ajax.decorators import ajax

from .forms import Login, NewGame, Konsonant
from .models import UserLogin, Game, Word

# Create your views here.

random_word = ""


def index(request):
    return render(request, 'user/index.html')


def new_user(request):
    if request.method == "POST":
        form = Login(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.loggedInAt = timezone.now()
            post.save()
            return redirect('users')
    else:
        form = Login()
        return render(request, 'user/login.html', {'form': form})


def users(request):
    newest_user = UserLogin.objects.order_by('-loggedInAt')[:5]
    template = loader.get_template('user/users.html')
    context = {
        'newest_user': newest_user,
    }
    return HttpResponse(template.render(context, request))


def new_game(request):
    if request.method == "POST":
        form = NewGame(request.POST)
        if form.is_valid():
            gm = form.save(commit=False)
            gm.date_played = timezone.now()
            gm.save()
            return redirect('game')
    else:
        form = NewGame
        return render(request, 'user/new_game.html', {'form': form})


def game(request):
    if request.method == 'POST':
        form = Konsonant(request.POST)
        if form.is_valid():
            print('form is valid')
            print(form.cleaned_data['konsonant'])
            guess_consonant(form.cleaned_data['konsonant'])
            return render(request, 'user/game.html')
        else:
            vals = ['10', '25', '50', '100', '500', 'x2', 'x4', 'Aussetzen', 'Bankrott']
            spinned = random.choice(vals)
            return render(request, 'user/game.html', {'form': form, 'spinned': spinned})
    else:
        return render(request, 'user/game.html')


def guess_consonant(request):
    """TODO"""


@ajax
def spin_wheel(request):
    vals = ['10', '25', '50', '100', '500', 'x2', 'x4', 'Aussetzen', 'Bankrott']
    spinned = random.choice(vals)
    print(spinned)
    return {'spinned': spinned}
