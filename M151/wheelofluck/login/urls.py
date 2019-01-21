from django.urls import path

from login import views

urlpatterns = [
    path('your_login', views.users, name='users'),
    path('users/', views.users, name='users'),
    path('', views.index, name='index'),
]
