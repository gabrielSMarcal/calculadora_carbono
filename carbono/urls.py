from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('calculadora/', views.calculadora, name='calculadora'),
    path('limpar_carro/', views.limpar_carro, name='limpar_carro'),
    path('limpar_energia/', views.limpar_energia, name='limpar_energia'),
    path('limpar_onibus/', views.limpar_onibus, name='limpar_onibus'),
    path('limpar_gas/', views.limpar_gas, name='limpar_gas'),
    path('limpar_sessao/', views.limpar_sessao, name='limpar_sessao'),
]

