from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.utils import timezone

from .forms import Login, NewGame
from .models import UserLogin, Game

# Create your views here.


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
    return render(request, 'user/game.html')
