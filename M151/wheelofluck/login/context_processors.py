from wheelofluck.login.models import Game


def high_scores(request):
    high_score_list = Game.objects.order_by('-amount_played')[:5]
    context = {
        'high_score_list': high_score_list,
    }
    return {context}
