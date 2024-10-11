from django.shortcuts import render, get_object_or_404

from .models import Carro, Energia
    


def index(request):
    return render(request, 'carbono/index.html')

def teste(request):
    return render(request, 'carbono/teste.html')

