from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Carro, Energia
import math


def index(request):
    return render(request, 'carbono/index.html')


def valor_da_tonelada(co):
    media_valor_credito = (70.10 * 5.6165)  # Média dos últimos 12 meses na bolsa de valores multiplicado pelo valor da média do euro
    valor = co * media_valor_credito
    return valor


def arvores(co):
    absorcao_co2 = 0.36  # Cálculo baseado do site IDESAM
    arvore = co / absorcao_co2
    return arvore


def carro(km_por_mes_str, carro_obj):
    km_por_mes = float(km_por_mes_str)

    try:
        consumo = km_por_mes / carro_obj.consumo
        emissao = consumo * carro_obj.emissao
        credito = emissao / 1000
        anual = credito * 12
        return (credito, anual)
    except (ZeroDivisionError, Carro.DoesNotExist) as e:
        print(f'Erro no cálculo: {e}')
        return None


def energia_kwh(kwh_usado, energia_obj):
    kwh_usado = float(kwh_usado)

    emissao = kwh_usado * energia_obj.emissao
    credito = emissao / 1000
    anual = credito * 12

    return (credito, anual)


def energia_reais(valor_da_conta, energia_obj):
    conversao = valor_da_conta / 0.37
    emissao = conversao * energia_obj.emissao
    credito = emissao / 1000
    anual = credito * 12

    return (credito, anual)


def teste(request):
    carros = Carro.objects.all()
    energias = Energia.objects.all()
    
    carro_resultado = None
    energia_resultado = None
    total_anual = None
    arvores_necessarias = None
    valor_tonelada = None

    if request.method == 'POST':
        if 'carro_tipo' in request.POST and 'km_por_mes' in request.POST:
            carro_tipo = request.POST['carro_tipo']
            km_por_mes = request.POST['km_por_mes']

            try:
                # Obtenha a instância do Carro correta aqui
                carro_obj = Carro.objects.get(tipo=carro_tipo)
                credito, anual = carro(km_por_mes, carro_obj)
                carro_resultado = {'credito': round(credito, 3), 'anual': round(anual,3)}
            except Carro.DoesNotExist:
                carro_resultado = {'error': f'Carro {carro_tipo} não encontrado.'}
            except (ValueError, AttributeError) as e:
                print(f"Erro no cálculo do carro: {e}")

        if 'energia_tipo' in request.POST:
            energia_tipo = request.POST['energia_tipo']

            # Obtenha a instância de Energia correta aqui
            energia_obj = Energia.objects.get(modo_de_calculo=energia_tipo)

            if energia_tipo == 'kwh' and kwh_usado:
                kwh_usado = request.POST.get('kwh_usado')
                if kwh_usado:
                    credito, anual = energia_kwh(kwh_usado, energia_obj)
                    energia_resultado = {'credito': round(credito, 3), 'anual': round(anual, 3)}
                    
            elif energia_tipo == 'conta' and valor_da_conta:
                valor_da_conta = request.POST.get('valor_da_conta')
                if valor_da_conta:
                    credito, anual = energia_reais(valor_da_conta, energia_obj)
                    energia_resultado = {'credito': credito, 'anual': anual}
            else:
                energia_resultado = {'error': 'Erro: Nenhum valor válido foi fornecido para o cálculo de energia.'}


        if carro_resultado or energia_resultado:
            total_anual = round((carro_resultado['anual'] or 0 + energia_resultado['anual'] or 0), 3)
            arvores_necessarias = math.ceil(arvores(total_anual))
            valor_tonelada = round(valor_da_tonelada(total_anual), 2)

    return render(request, 'carbono/teste.html', {
        'carro_resultado': carro_resultado,
        'energia_resultado': energia_resultado,
        'total_anual': total_anual,
        'arvores_necessarias': arvores_necessarias,
        'valor_tonelada': valor_tonelada,
        'carros': carros,
        'energias': energias,
    })