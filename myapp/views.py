
from django.shortcuts import render

def accueil(request):
    return render(request, 'myapp/accueil.html')

def apropos(request):
    return render(request, 'myapp/apropos.html')
