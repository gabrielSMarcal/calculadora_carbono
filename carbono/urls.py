from django.urls import path

from . import views

'''
DEFINIÇÃO DOS CAMINHOS A SEREM DIRECIONADOS PARA ACESSO ÀS PÁGINAS, PODENDO SER DE UMA PÁGINA À OUTRA, OU REINÍCIO DE PÁGINA
'''

urlpatterns = [
    path('', views.index, name='index'),                            # Direcionamento 
    path('calculadora/', views.calculadora, name='calculadora'),    # para as páginas
    path('limpar_carro/', views.limpar_carro, name='limpar_carro'),            # Todas as páginas
    path('limpar_energia/', views.limpar_energia, name='limpar_energia'),      # em diante representam
    path('limpar_onibus/', views.limpar_onibus, name='limpar_onibus'),         # reload da página,
    path('limpar_gas/', views.limpar_gas, name='limpar_gas'),                  # pois está havendo
    path('limpar_sessao/', views.limpar_sessao, name='limpar_sessao'),         # alguma limpeza de calculadora
]

