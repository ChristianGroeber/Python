from django.conf import settings
from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:projekt_id>/', views.detail, name='detail'),
    url(r'^froala_editor/', include('froala_editor.urls')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root', settings.STATIC_ROOT}
        ),
]
