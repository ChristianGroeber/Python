from login.models import Game


def high_score_list(request):
    return {
        'high_score_list': Game.objects.order_by('-amount_played')[:5]
    }


def spinned(request):
    return {}
