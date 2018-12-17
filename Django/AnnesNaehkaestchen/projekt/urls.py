from AnnesNaehkaestchen import settings
from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:projekt_id>/', views.detail, name='detail'),
    url(r'^froala_editor/', include('froala_editor.urls')),
    path('neu', views.kommentieren, name='kommentieren'),
]
