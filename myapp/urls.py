
from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('bonjour/', views.accueil, name='bonjour'),
    path('apropos/', views.apropos, name='apropos'),
]
