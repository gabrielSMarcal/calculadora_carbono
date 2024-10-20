from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
import math

from .models import Carro, Energia, Onibus, Gas

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

def carro(km_por_mes, carro_obj):
    km_por_mes = float(km_por_mes)
    emissao = (km_por_mes / carro_obj.consumo) * carro_obj.emissao
    credito = emissao / 1000
    anual = credito * 12
    
    return (credito, anual)




def energia_kwh(kwh_usado, energia_obj):
    kwh_usado = float(kwh_usado)
    
    emissao = kwh_usado * energia_obj.emissao
    credito = emissao / 1000
    anual = credito * 12
    
    return (credito, anual)


def energia_reais(valor_da_conta, energia_obj):
    valor_da_conta = float(valor_da_conta)
    emissao = valor_da_conta * energia_obj.emissao
    credito = emissao / 1000
    anual = credito * 12
    
    return (credito, anual)

def onibus(km_por_mes_onibus):
    km_por_mes_onibus = float(km_por_mes_onibus)
    emissao = (km_por_mes_onibus / 2.63) * 2.8 / 40  # Média de 40 passageiros por ônibus
    credito = (emissao / 1000)
    anual = credito * 12

    return (credito, anual)


def gas_botijao(botijao, gas_obj):
    botijao = float(botijao) 
    credito = (botijao * 40.15) / 1000
    anual = credito * 12

    return (credito, anual)

 
def gas_encanado(area, gas_obj):
    area = float(area) 
    credito = (area * 1.997) / 1000
    anual = credito * 12

    return (credito, anual)


def teste(request):
    carros = Carro.objects.all()
    energias = Energia.objects.all()
    gases = Gas.objects.all()

    if 'carro_resultado' not in request.session:
        request.session['carro_resultado'] = None
    if 'energia_resultado' not in request.session:
        request.session['energia_resultado'] = None
    if 'onibus_resultado' not in request.session:
        request.session['onibus_resultado'] = None
    if 'gas_resultado' not in request.session:
        request.session['gas_resultado'] = None

    carro_resultado = request.session['carro_resultado']
    energia_resultado = request.session['energia_resultado']
    onibus_resultado = request.session['onibus_resultado']
    gas_resultado = request.session['gas_resultado']
    
    total_anual = 0
    arvores_necessarias = 0
    valor_tonelada = 0

    if request.method == 'POST':
        carro_tipo = request.POST.get('carro_tipo')
        km_por_mes = request.POST.get('km_por_mes')
        energia_tipo = request.POST.get('energia_tipo')

        km_por_mes_onibus = request.POST.get('km_por_mes_onibus')
        gas_tipo = request.POST.get('gas_tipo')
        botijao_gas = request.POST.get('botijao_gas')
        volume_gas = request.POST.get('volume_gas')

        if carro_tipo and km_por_mes:
            try:
                km_por_mes = float(km_por_mes)
                if km_por_mes < 0:
                    raise ValueError("Km por mês não pode ser negativo.")
                carro_obj = Carro.objects.get(tipo=carro_tipo)
                credito, anual = carro(km_por_mes, carro_obj)
                carro_resultado = {'credito': round(credito, 3), 'anual': round(anual, 3)}
                request.session['carro_resultado'] = carro_resultado
            except ValueError as e:
                return HttpResponse(str(e), status=400)

        if energia_tipo:
            try:
                energia_obj = Energia.objects.get(modo_de_calculo=energia_tipo)
                if energia_tipo == 'Kwh':
                    kwh_usado = request.POST.get('kwh_usado')
                    if kwh_usado:
                        kwh_usado = float(kwh_usado)
                        if kwh_usado < 0:
                            raise ValueError("kWh Usado não pode ser negativo.")
                        credito, anual = energia_kwh(kwh_usado, energia_obj)
                        energia_resultado = {'credito': round(credito, 3), 'anual': round(anual, 3)}
                        request.session['energia_resultado'] = energia_resultado
                        
                elif energia_tipo == 'Conta de Luz':
                    valor_da_conta = request.POST.get('valor_da_conta')
                    if valor_da_conta:
                        valor_da_conta = float(valor_da_conta)
                        if valor_da_conta < 0:
                            raise ValueError("Valor da Conta de Luz não pode ser negativo.")
                        credito, anual = energia_reais(valor_da_conta, energia_obj)
                        energia_resultado = {'credito': round(credito, 3), 'anual': round(anual, 3)}
                        request.session['energia_resultado'] = energia_resultado
                        
                else:
                    energia_resultado = {'error': 'Erro: Nenhum valor válido foi fornecido para o cálculo de energia.'}
            except ObjectDoesNotExist:
                energia_resultado = {'error': 'Erro: Tipo de energia não encontrado.'}
                
        if km_por_mes_onibus:
            try:
                km_por_mes_onibus = float(km_por_mes_onibus)
                if km_por_mes_onibus < 0:
                    raise ValueError('Km por mês não pode ser negativo.')
                credito, anual = onibus(km_por_mes_onibus)
                onibus_resultado = {'credito': round(credito, 3), 'anual': round(anual, 3)}
                request.session['onibus_resultado'] = onibus_resultado
            except ValueError as e:
                return HttpResponse(str(e), status=400)
            except ObjectDoesNotExist:
                onibus_resultado = {'error': 'Erro: Tipo de ônibus não encontrado.'}
        
        if gas_tipo:
            try:
                gas_obj = Gas.objects.get(modo_de_calculo=gas_tipo)
                if gas_tipo == 'Botijão' and botijao_gas:
                    botijao_gas = float(botijao_gas)
                    if botijao_gas < 0:
                        raise ValueError('Botijão de gás não pode ser negativo.')
                    credito, anual = gas_botijao(botijao_gas, gas_obj)
                    gas_resultado = {'credito': round(credito, 3), 'anual': round(anual, 3)}
                    request.session['gas_resultado'] = gas_resultado
                elif gas_tipo == 'Encanado' and volume_gas:
                    volume_gas = float(volume_gas)
                    if volume_gas < 0:
                        raise ValueError('Volume de gás não pode ser negativo.')
                    credito, anual = gas_encanado(volume_gas, gas_obj)
                    gas_resultado = {'credito': round(credito, 3), 'anual': round(anual, 3)}
                    request.session['gas_resultado'] = gas_resultado
                else:
                    gas_resultado = {'error': 'Erro: Nenhum valor válido foi fornecido para o cálculo de gás.'}
            except ObjectDoesNotExist:
                gas_resultado = {'error': 'Erro: Tipo de gás não encontrado.'}

    if carro_resultado and 'anual' in carro_resultado:
        total_anual += carro_resultado['anual']
    if energia_resultado and 'anual' in energia_resultado:
        total_anual += energia_resultado['anual']
    if onibus_resultado and 'anual' in onibus_resultado:
        total_anual += onibus_resultado['anual']
    if gas_resultado and 'anual' in gas_resultado:
        total_anual += gas_resultado['anual']

    if total_anual > 0:        
        arvores_necessarias = math.ceil(arvores(total_anual))
        valor_tonelada = round(valor_da_tonelada(total_anual), 2)

    return render(request, 'carbono/teste.html', {
        'carro_resultado': carro_resultado,
        'energia_resultado': energia_resultado,
        'onibus_resultado': onibus_resultado,
        'gas_resultado': gas_resultado,
        'total_anual': round(total_anual, 3),
        'arvores_necessarias': arvores_necessarias,
        'valor_tonelada': valor_tonelada,
        'carros': carros,
        'energias': energias,
        'onibus': onibus,
        'gases': gases,
    })
    

def limpar_sessao(request):
    request.session['carro_resultado'] = None
    request.session['energia_resultado'] = None
    request.session['onibus_resultado'] = None
    request.session['gas_resultado'] = None
    request.session.flush()
    return redirect('teste')