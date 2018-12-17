from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from .models import Projekt
from .forms import Kommentar

def index(request):
    neuestes_projekt = Projekt.objects.order_by('-veroeffentlicht')[:5]
    template = loader.get_template('projekt/index.html')
    context = {
        'neuestes_projekt': neuestes_projekt,
    }
    return HttpResponse(template.render(context, request))


def detail(request, projekt_id):
    try:
        projekt = Projekt.objects.get(pk=projekt_id)
    except Projekt.DoesNotExist:
        raise Http404("Dieses Projekt existiert nicht")
    return render(request, 'projekt/detail.html', {'projekt': projekt})


def kommentieren(request):
    form = Kommentar()
    return render(request, 'projekt/kommentar.html', {'form': form})
