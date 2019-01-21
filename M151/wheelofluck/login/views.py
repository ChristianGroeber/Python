
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .forms import Login
from .models import UserLogin

# Create your views here.


def index(request):
    form = Login()
    return render(request, 'user/login.html', {'form': form})


def users(request):
    newest_user = UserLogin.objects.order_by('-loggedInAt')[:5]
    template = loader.get_template('user/users.html')
    context = {
        'newest_user': newest_user,
    }
    return HttpResponse(template.render(context, request))

