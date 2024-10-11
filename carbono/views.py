from django.shortcuts import render, get_object_or_404

from .models import Carro, Energia
import math
    


def index(request):
    return render(request, 'carbono/index.html')


# Função para calcular o valor monetário
def valor_da_tonelada(co):

    media_valor_credito = (70.10 * 5.6165) # Média dos últimos 12 meses na bolsa de valores multiplicado pelo valor da média do euro
    valor = co * media_valor_credito

    return valor

# Função de compensação das Árvores
def arvores(co):
    absorcao_co2 = 0.36485 # Cálculo baseado do site IDESAM
    arvore = co / absorcao_co2

    return arvore

def teste(request):
    carros = Carro.objects.all()
    energias = Energia.objects.all()
    dados_carro = {}
    dados_energia = {}
    error_message = None

    if request.method == 'POST':
        # Handle car data
        if 'km_por_mes' in request.POST:
          try:
              for carro in carros:
                  km_por_mes = float(request.POST.get(f"km_por_mes_{carro.id}"))
                  if km_por_mes < 0:  # Validate input
                      error_message = "Kilometragem inválida."
                      return render(request, "carbono/teste.html", {"carros": carros, "energias": energias, "error_message": error_message})


                  CO_GASOLINA = carro.emissao  # Use the model data
                  consumo = km_por_mes / 10.6
                  emissao = consumo * CO_GASOLINA
                  credito = emissao / 1000
                  anual = credito * 12
                  dados_carro[carro.legenda] = {
                      "consumo": round(consumo, 3),
                      "emissao": round(emissao, 3),
                      "credito": round(credito, 3),
                      "anual": round(anual, 3),
                  }
          except (ValueError, TypeError):
              error_message = "Insira um valor numérico válido para a quilometragem mensal."
              return render(request, "carbono/teste.html", {"carros": carros, "energias": energias, "error_message": error_message})

        #Algoritmo de Energia
        if 'tipo_de_energia' in request.POST:
            energia_selecionada = get_object_or_404(Energia, pk=request.POST['tipo_de_energia'])
            try:
                if energia_selecionada.modo_de_calculo == 'kWh':
                    kwh_usado = float(request.POST.get('kwh_usado'))
                    CO_ENERGIA = energia_selecionada.emissao
                    emissao = kwh_usado * CO_ENERGIA
                    credito = emissao / 1000
                    anual = credito * 12
                    dados_energia = {
                        'tipo_energia': energia_selecionada.legenda,
                        'co2_por_mes': round(credito, 3),
                        'co2_por_ano': round(anual, 3),
                        'arvores_a_plantar': math.ceil(arvores(anual)),
                        'valor_credito': round(valor_da_tonelada(anual), 2),
                    }
                elif energia_selecionada.modo_de_calculo == 'Conta de Energia':
                    valo_da_conta= float(request.POST.get('valor_da_conta'))
                    CO_ENERGIA = energia_selecionada.emissao
                    conversao = valo_da_conta / 0.37
                    emissao = conversao * CO_ENERGIA
                    credito = emissao / 1000
                    anual = credito * 12
                    dados_energia = {
                        'tipo_energia': energia_selecionada.legenda,
                        'co2_por_mes': round(credito, 3),
                        'co2_por_ano': round(anual, 3),
                        'arvores_a_plantar': math.ceil(arvores(anual)),
                        'valor_credito': round(valor_da_tonelada(anual), 2),
                    }
            except (ValueError, TypeError):
                error_message = 'Insira um valor numérico válido para os dados de energia'

    return render(request, "carbono/teste.html", {"carros": carros, "energias": energias, "dados_carro": dados_carro, "dados_energia": dados_energia, "error_message": error_message})
