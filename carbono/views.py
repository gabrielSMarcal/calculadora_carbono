from django.shortcuts import render


def index(request):
    return render(request, 'carbono/index.html')

def teste(request):
    return render(request, 'carbono/teste.html')
