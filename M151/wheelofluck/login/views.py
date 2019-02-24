import random

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.utils import timezone

from .forms import Login, NewGame, Konsonant
from .models import UserLogin, Game, Word, PlayerWord
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
    word = Game.objects.get(id=id_of_player).wort
    a = PlayerWord(word=word)
    a.save()
    print(a.word)
    arr = []
    output = ""
    if word.__contains__(' '):
        arr = word.split()
    result = ""
    spinned = 0
    for x in arr:
        for i in range(0, len(x)):
            output += "_ "
        output += "-"
    if request.method == 'POST':
        form = Konsonant(request.POST)
        if form.is_valid():
            print('form is valid')
            if not is_consonant(form.cleaned_data['konsonant']):
                result = "This isn't a consonant"
            elif guess_consonant(form.cleaned_data['konsonant'], word):
                result += str(word.count(form.cleaned_data['konsonant']))
                PlayerWord.found_consonants.append(form.cleaned_data['konsonant'])
                for i in range(1, word.count(form.cleaned_data['konsonant']) + 1):
                    print('a: ' + str(get_index_of_substring(form.cleaned_data['konsonant'], word, i)))
            else:
                result += "The consonant " + form.cleaned_data['konsonant'] + " wasn't found in the word."
            result += str(PlayerWord.found_consonants)
            return render(request, 'user/game.html', {'output': output, 'result': result})
        else:
            vals = ['10', '25', '50', '100', '500', 'x2', 'x4', 'Aussetzen', 'Bankrott']
            spinned = random.choice(vals)
            return render(request, 'user/game.html', {'form': form, 'spinned': spinned,
                                                      'output': output, 'result': result})
    else:
        return render(request, 'user/game.html', {'output': output, 'result': result})


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


def spin_wheel(request):
    vals = ['10', '25', '50', '100', '500', 'x2', 'x4', 'Aussetzen', 'Bankrott']
    spinned = random.choice(vals)
    print(spinned)
    return {'spinned': spinned}
