from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
import math

from .models import Carro, Energia



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
    valor_da_conta = float(valor_da_conta)
    
    conversao = valor_da_conta / 0.37
    emissao = conversao * energia_obj.emissao
    credito = emissao / 1000
    anual = credito * 12

    return (credito, anual)


def teste(request):
    carros = Carro.objects.all()
    energias = Energia.objects.all()
    
    if 'carro_resultado' not in request.session:
        request.session['carro_resultado'] = None
    if 'energia_resultado' not in request.session:
        request.session['energia_resultado'] = None
    
    carro_resultado = request.session['carro_resultado']
    energia_resultado = request.session['energia_resultado']
    total_anual = None
    arvores_necessarias = None
    valor_tonelada = None

    if request.method == 'POST':
        carro_tipo = request.POST.get('carro_tipo')
        km_por_mes = request.POST.get('km_por_mes')
        energia_tipo = request.POST.get('energia_tipo')
                
        if carro_tipo and km_por_mes:
            carro_obj = Carro.objects.get(tipo=carro_tipo)
            credito, anual = carro(km_por_mes, carro_obj)
            carro_resultado = {'credito': round(credito, 3), 'anual': round(anual, 3)}
            request.session['carro_resultado'] = carro_resultado
            
        else:
            energia_resultado = {'error': 'Modo de cálculo não encontrado'}

        
        if energia_tipo:
            try:
                energia_obj = Energia.objects.get(modo_de_calculo=energia_tipo)
                if energia_tipo == 'Kwh':
                    kwh_usado = request.POST.get('kwh_usado')
                    if kwh_usado:
                        credito, anual = energia_kwh(kwh_usado, energia_obj)
                        energia_resultado = {'credito': round(credito, 3), 'anual': round(anual, 3)}
                        request.session['energia_resultado'] = energia_resultado
                elif energia_tipo == 'Conta de Luz':
                    valor_da_conta = request.POST.get('valor_da_conta')
                    if valor_da_conta:
                        credito, anual = energia_reais(valor_da_conta, energia_obj)
                        energia_resultado = {'credito': round(credito, 3), 'anual': round(anual, 3)}
                        request.session['energia_resultado'] = energia_resultado
                else:
                    energia_resultado = {'error': 'Modo de cálculo não encontrado'}
            except ObjectDoesNotExist:
                energia_resultado = {'error': 'Modo de cálculo não encontrado'}
            
        if carro_resultado or energia_resultado:
            total_anual = round((carro_resultado['anual'] if carro_resultado else 0) + (energia_resultado['anual'] if energia_resultado else 0), 3)
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
    
def limpar_sessao(request):
        request.session['carro_resultado'] = None
        request.session['energia_resultado'] = None
        return redirect('teste')