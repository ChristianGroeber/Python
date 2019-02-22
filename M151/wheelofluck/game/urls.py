from django.urls import path

from game import views

urlpatterns = [
    path('game/konsonant', views.spin_wheel, name='konsonant'),
    path('game/betrag/', views.spin_wheel, name='betrag'),
    path('game/', views.game, name='game'),
    path('', views.index, name='index'),
]
