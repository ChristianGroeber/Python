from django.urls import path

from login import views

urlpatterns = [
    path('game/risiko/<answer>/', views.risiko),
    path('game/risiko/', views.risiko, name='game.risiko'),
    path('game/result/', views.result, name='game.result'),
    path('game/solve/', views.solve, name='game.solve'),
    path('game/<amount>/', views.redirect_game),
    path('game/', views.game, name='game'),
    path('new_game/', views.new_game, name='new_game'),
    path('new_user/', views.new_user, name='new_user'),
    path('users/new_user/your_login', views.users, name='users/'),
    path('users/', views.users, name='users'),
    path('', views.index, name='index'),
]
