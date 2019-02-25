import random

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.utils import timezone

from .forms import Login, NewGame, Konsonant
from .models import UserLogin, Game, Word, PlayerWord, Category
from .context_processors import IdOfPlayer

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


global id_of_player
global times_guessed
times_guessed = 0
global playing


def new_game(request):
    if request.method == "POST":
        form = NewGame(request.POST)
        if form.is_valid():
            global id_of_player
            gm = Game.create(form.cleaned_data['player'])
            gm.save()
            id_of_player = gm.id
            print('id: ' + str(id_of_player))
            return redirect('game')
    else:
        form = NewGame
        return render(request, 'user/new_game.html', {'form': form})


def game(request):
    global id_of_player
    global times_guessed
    global playing
    game_object = Game.objects.get(id=id_of_player)
    word = game_object.wort.word
    output = game_object.output
    result = ""
    credit = Game.objects.get(id=id_of_player).amount_played
    dev_info = ["word: " + word, "player id: " + str(game_object.id),
                'Times guessed: ' + str(times_guessed),
                'Guthaben: ' + str(game_object.amount_played), "Result: " + result]
    category = Word.objects.get(word=word).category
    can_play = True
    if request.method == 'POST':
        form = Konsonant(request.POST)
        if form.is_valid():
            print('form is valid')
            konsonant = form.cleaned_data['konsonant']
            if not any(konsonant in s for s in game_object.found_consonants):
                if not is_consonant(konsonant):
                    result = "This isn't a consonant"
                elif guess_consonant(konsonant, word):
                    result += str(word.count(konsonant))
                    Game.found_consonants.append(konsonant)
                    output = Game.generate_output(Game.objects.get(id=id_of_player), konsonant)
                    played = word.count(konsonant) * int(playing) + Game.objects.get(pk=id_of_player).amount_played
                    Game.objects.filter(pk=id_of_player).update(amount_played=played)
                    credit = played
                else:
                    times_guessed = times_guessed + 1
                    if times_guessed >= 3:
                        return redirect("/")
                    result += "The consonant " + konsonant + " wasn't found in the word. You have " \
                              + str(3 - times_guessed) + " guesses left."
                result += str(Game.found_consonants)
            else:
                result += "Diesen Konsonanten haben Sie bereits erraten."
            return render(request, 'user/game.html', {'output': output, 'dev_info': dev_info, 'credit': credit,
                                                      'can_play': can_play, 'category': category})
        else:
            vals = ['10', '25', '50', '100', '500', 'Risiko', 'Bankrott']
            spinned = random.choice(vals)
            playing = spinned
            if playing == 'Risiko':
                tmp = "TODO: implement Risiko function"
                print(tmp)
                dev_info.append(tmp)
                answers = list(Game.objects.get(pk=id_of_player).wort.answer.all())
                print(answers[0])
            else:
                try:
                    a = int(playing)
                except ValueError:
                    can_play = False
            return render(request, 'user/game.html', {'form': form, 'spinned': spinned,
                                                      'output': output, 'dev_info': dev_info, 'credit': credit,
                                                      'can_play': can_play})
    else:
        return render(request, 'user/game.html', {'output': output, 'dev_info': dev_info, 'credit': credit,
                                                  'can_play': can_play})


def guess_consonant(str, word):
    consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x',
                  'y', 'z']
    return word.__contains__(str)


def get_index_of_substring(sub, word, occurance):
    arr = list(word)
    x = 0
    found = 0
    for i in arr:
        x = x + 1
        if i == sub:
            found = found + 1
            if found == occurance:
                return x


def is_consonant(str):
    consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x',
                  'y', 'z']
    return any(str in s for s in consonants)
