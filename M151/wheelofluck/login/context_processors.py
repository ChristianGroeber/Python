from login.models import Game


def high_score_list(request):
    return {
        'high_score_list': Game.objects.order_by('-amount_played')[:5]
    }


def stats(request):
    return {
        # 'kategorie': Game.objects.get(pk=IdOfPlayer.current_player_id(request)['id']).wort.category
    }


def spinned(request):
    return {}


class IdOfPlayer:
    global id_of_player
    id_of_player = 0

    def current_player_id(request):
        return {'id': id_of_player}

    def set_id_of_player(num):
        global id_of_player
        id_of_player = num
