from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('teste/', views.teste, name='teste'),
    path('limpar_sessao/', views.limpar_sessao, name='limpar_sessao'),
]

