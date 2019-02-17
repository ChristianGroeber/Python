from django.shortcuts import render, redirect

from TinderCheck.Checker.models import Check
from .forms import PostForm


# Create your views here.

def IndexView(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            if Check.check_if_match:
                return redirect
            return redirect('result')
    else:
        form = PostForm()
    return render(request, 'Checker/index.html', {'form': form})


def match(request):
    return render(request, 'Checker/match.html', {})




def result(request):
    return render(request, 'Checker/result.html', {})
