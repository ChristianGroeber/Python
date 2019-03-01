import random
from .context_processors import IdOfPlayer
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.utils import timezone

from .forms import Login, NewGame, Konsonant, Solve, Setzen
from .models import UserLogin, Game, Word, PlayerWord, Category, Answer

# Create your views here.

random_word = ""


def index(request):
    return render(request, 'user/index.html')


def new_user(request):
    if request.method == "POST":
        form = Login(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.loggedInAt = timezone.now()
            user.save()
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


global times_guessed
times_guessed = 0
global playing
global stats
stats = {'kategorie': "", 'guthaben': "", 'fehler': ""}
global stage
stage = 1


def new_game(request):
    if request.method == "POST":
        form = NewGame(request.POST)
        if form.is_valid():
            gm = Game.create(form.cleaned_data['player'])
            gm.save()
            id = gm.id
            print('id: ' + str(id))
            return redirect('game', id)
    else:
        form = NewGame
        return render(request, 'user/new_game.html', {'form': form})


def game(request, id):
    global times_guessed
    global playing
    global stats
    global stage
    stats['fehler'] = times_guessed
    IdOfPlayer.set_id_of_player(id)
    game_object = Game.objects.get(id=id)
    word = game_object.wort.word
    output = game_object.output
    result = ""
    credit = Game.objects.get(id=id).amount_played
    print(int(credit))
    dev_info = ["word: " + word, "player id: " + str(game_object.id),
                'Times guessed: ' + str(times_guessed),
                'Guthaben: ' + str(game_object.amount_played), "Result: " + result]
    stats['kategorie'] = Word.objects.get(word=word).category
    can_play = True
    if stage == 2:
        stage = 1
    if request.method == 'POST':
        form = Konsonant(request.POST)
        if form.is_valid() and not playing == 'Risiko':
            print('form is valid')
            konsonant = form.cleaned_data['konsonant'].lower()
            if not any(konsonant in s for s in game_object.found_consonants):
                if not is_consonant(konsonant):
                    result = "This isn't a consonant"
                elif guess_consonant(konsonant, word.lower()):
                    result += str(word.count(konsonant))
                    Game.found_consonants.append(konsonant)
                    output = Game.generate_output(Game.objects.get(id=id), konsonant)
                    played = word.count(konsonant) * int(playing) + Game.objects.get(pk=id).amount_played
                    Game.objects.filter(pk=id).update(amount_played=played)
                    stats['guthaben'] = played
                    credit = played
                    spielrunden = Game.objects.get(pk=id).spielrunden
                    Game.objects.filter(pk=id).update(spielrunden=int(spielrunden) + 1)
                else:
                    times_guessed = times_guessed + 1
                    if times_guessed >= 3:
                        return redirect("/")
                    result += "The consonant " + konsonant + " wasn't found in the word. You have " \
                              + str(3 - times_guessed) + " guesses left."
                result += str(Game.found_consonants)
                stage = 1
            else:
                stage = 2
                result += "Diesen Konsonanten haben Sie bereits erraten."
            return render(request, 'user/game.html', {'output': output, 'dev_info': dev_info, 'credit': credit,
                                                      'can_play': can_play, 'stats': stats, 'stage': stage, 'id': id})
        else:
            vals = ['10', '25', '50', '100', '500', 'Risiko']
            spinned = random.choice(vals)
            playing = spinned
            if playing == 'Risiko':
                return redirect("game.risiko", id)
            else:
                try:
                    int(playing)
                except ValueError:
                    can_play = False
            stage = 2
            return render(request, 'user/game.html', {'form': form, 'spinned': spinned,
                                                      'output': output, 'dev_info': dev_info, 'credit': credit,
                                                      'can_play': can_play, 'stats': stats, 'stage': stage, 'id': id})
    else:
        stage = 1
        return render(request, 'user/game.html', {'output': output, 'dev_info': dev_info, 'credit': credit,
                                                  'can_play': can_play, 'stats': stats, 'stage': stage, 'id': id})


global betrag_gesetzt


def risiko(request, answer=None, id=None):
    global stats
    global betrag_gesetzt
    form = Setzen(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            print('form is valid')
            try:
                if int(form.cleaned_data['betrag']) <= Game.objects.get(pk=id).amount_played:
                    frage = Game.objects.get(pk=id).wort
                    answers = list(frage.answer.all())
                    betrag_gesetzt = int(form.cleaned_data['betrag'])
                    print(str(betrag_gesetzt))
                    return render(request, 'user/risiko.html', {'frage': frage, 'antwort': answers, 'possible': True,
                                                                'stats': stats, 'id': id})
            except TypeError:
                print(TypeError.with_traceback())
    elif answer:
        global won
        print(answer)
        print(id)
        won = Answer.objects.get(text=answer).is_correct
        if won:
            a = Game.objects.get(pk=id).amount_played
            print(str(a))
            Game.objects.filter(pk=id).update(amount_played=int(a) + int(betrag_gesetzt))
        return redirect('game.result', id)
    return render(request, 'user/risiko.html', {'possible': False, 'form': form, 'stats': stats, 'id': id})


global won
won = False


def solve(request, id):
    global won
    global stats
    form = Solve(request.POST)
    result = ["Hey"]
    if form.is_valid():
        won = check_if_correct_phrase(form.cleaned_data['Question'], id)
        return redirect('game.result', id)
    return render(request, 'user/solve.html', {'form': form, 'stats': stats, 'id': id})


def result(request, id):
    global won
    result = ""
    if won:
        result = "Gratuliere, Sie haben " + str(Game.objects.get(pk=id).amount_played) + " gewonnen"
    else:
        result = "Sie haben leider verloren."
    return render(request, "user/result.html", {'result': result})


def guess_consonant(str, word):
    consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x',
                  'y', 'z']
    return word.__contains__(str)


def check_if_correct_phrase(phrase, id):
    print(phrase)
    print(Game.objects.get(pk=id).wort)
    return phrase.lower() == str(Game.objects.get(pk=id).wort).lower()


def check_answer(answer, id):
    return answer.__contains__([Game.objects.get(pd=id).wort.answer.all()])


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
