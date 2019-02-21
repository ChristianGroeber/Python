from django.urls import path

from login import views

urlpatterns = [
    path('game/konsonant', views.spin_wheel, name='konsonant'),
    path('new_game/user/betrag', views.game, name='betrag'),
    path('new_game/', views.new_game, name='new_game'),
    path('new_user/', views.new_user, name='new_user'),
    path('users/new_user/your_login', views.users, name='users/'),
    path('users/', views.users, name='users'),
    path('', views.index, name='index'),
]
