from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from math import ceil
import requests
import os

from .models import Carro, Energia, Gas


'''
************************************** CONSTANTES **************************************
'''
MEDIA_CC = 63.87
CUSTO_POR_ARVORE = 35
CONV_ENERGIA = 0.37

# URL da API e chave de acesso
API_KEY = os.getenv('EXCHANGE_RATE_API_KEY')
API_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/EUR"

def get_euro_exchange_rate():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        return data['conversion_rates']['BRL']  # Supondo que você quer a taxa de EUR para BRL
    except requests.RequestException as e:
        print(f"Erro ao obter a taxa de câmbio: {e}")
        return None

# Atualizando a constante com o valor atual do euro
MEDIA_EURO = get_euro_exchange_rate() or 6.5


# Renderização da página inicial
def index(request):
    return render(request, 'carbono/index.html')

'''
************************************** FUNÇÕES DAS CALCULADORAS **************************************
'''

# Função para cálculo do valor do CC futuro baseado na TCO2
def valor_da_tonelada(co):
    media_valor_credito = (MEDIA_CC * MEDIA_EURO)  # Média dos últimos 12 meses
    
    valor = co * media_valor_credito
    return valor

# Função para cálculo de índice de árvores necessárias para compensar, baseado na TCO2
def arvores(co):
    ABSORCAO = 0.37  # Cálculo baseado do site IDESAM
    
    arvore = co / ABSORCAO
    custo = ceil(arvore) * CUSTO_POR_ARVORE 
    return (arvore, custo)

'''
******************* FUNÇÕES PARA CÁLCULO DE CARBONO, RETORNANDO SEMPRE O VALOR MENSAL (credito) E ANUAL (anual) *******************
'''

# Função para calcular carbono de carro, baseado na quilometragem por mês.
def carro(km_por_mes, carro_obj):
    km_por_mes = float(km_por_mes)
    emissao = (km_por_mes / carro_obj.consumo) * carro_obj.emissao
    credito = emissao / 1000
    anual = credito * 12
    
    return (credito, anual)

# Função para calcular carbono de energia, baseada na quantidade de Kilowatts por hora no mês.
def energia_kwh(kwh_usado, energia_obj):
    kwh_usado = float(kwh_usado)    
    emissao = kwh_usado * energia_obj.emissao
    credito = emissao / 1000
    anual = credito * 12
    
    return (credito, anual)

# Função para calcular carbono de energia, baseada no valor monetário da conta de luz do usuário.
def energia_reais(valor_da_conta, energia_obj):
    valor_da_conta = float(valor_da_conta)
    conversao = valor_da_conta / CONV_ENERGIA
    emissao = conversao * energia_obj.emissao
    credito = emissao / 1000
    anual = credito * 12
    
    return (credito, anual)

# Função para calcular carbono de ônibus, baseado na quilometragem mensal usada pelo usuário, dividido por uma média de passageiros.
def onibus(km_por_mes_onibus, carro_obj):
    km_por_mes_onibus = float(km_por_mes_onibus)
    emissao = (km_por_mes_onibus / carro_obj.consumo) * carro_obj.emissao / 40  # Média de 40 passageiros por ônibus
    credito = emissao / 1000
    anual = credito * 12

    return (credito, anual)

# Função para calcular carbono de gás de cozinha, baseado no numero de botijões (13kg) usados por mês.
def gas_botijao(botijao, gas_obj):
    botijao = float(botijao) 
    credito = (botijao * gas_obj.emissao) / 1000
    anual = credito * 12

    return (credito, anual)

# Função para calcular barbono de gás de cozinha, baseado no valor em m³ de gás encanado usado por mês.
def gas_encanado(area, gas_obj):
    area = float(area) 
    credito = (area * gas_obj.emissao) / 1000
    anual = credito * 12

    return (credito, anual)

# Renderização da página da calculadora, absorvendo os valores inseridos no site para retornar os resultados.
def calculadora(request):
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
    custo_arvores = 0
    valor_tonelada = 0
    

    # Condição para receber informações no forms
    if request.method == 'POST':
        carro_tipo = request.POST.get('carro_tipo')
        km_por_mes = request.POST.get('km_por_mes')
        energia_tipo = request.POST.get('energia_tipo')
        km_por_mes_onibus = request.POST.get('km_por_mes_onibus')
        gas_tipo = request.POST.get('gas_tipo')
        botijao_gas = request.POST.get('botijao_gas')
        volume_gas = request.POST.get('volume_gas')

        # Cálculo de carro
        if carro_tipo and km_por_mes:
            try:
                km_por_mes = float(km_por_mes)
                if km_por_mes < 0:
                    raise ValueError("Km por mês não pode ser negativo.")
                carro_obj = Carro.objects.get(tipo=carro_tipo)
                credito, anual = carro(km_por_mes, carro_obj)
                if credito > 0:
                    carro_resultado = {'credito': round(credito, 3), 'anual': round(anual, 3)}
                else:
                    carro_resultado = None
                request.session['carro_resultado'] = carro_resultado
            except ValueError as e:
                return HttpResponse(str(e), status=400)

        # Cálculo de energia
        if energia_tipo:
            try:
                energia_obj = Energia.objects.get(modo_de_calculo=energia_tipo)
                if energia_tipo == 'kWh':
                    kwh_usado = request.POST.get('kwh_usado')
                    if kwh_usado:
                        kwh_usado = float(kwh_usado)
                        if kwh_usado < 0:
                            raise ValueError("kWh Usado não pode ser negativo.")
                        credito, anual = energia_kwh(kwh_usado, energia_obj)
                        if credito > 0:
                            energia_resultado = {'credito': round(credito, 3), 'anual': round(anual, 3)}
                        else:
                            energia_resultado = None
                        request.session['energia_resultado'] = energia_resultado
                        
                elif energia_tipo == 'Conta de Luz':
                    valor_da_conta = request.POST.get('valor_da_conta')
                    if valor_da_conta:
                        valor_da_conta = float(valor_da_conta)
                        if valor_da_conta < 0:
                            raise ValueError("Valor da Conta de Luz não pode ser negativo.")
                        credito, anual = energia_reais(valor_da_conta, energia_obj)
                        if credito > 0:
                            energia_resultado = {'credito': round(credito, 3), 'anual': round(anual, 3)}
                        else:
                            energia_resultado = None
                        request.session['energia_resultado'] = energia_resultado
                        
                else:
                    energia_resultado = {'error': 'Erro: Nenhum valor válido foi fornecido para o cálculo de energia.'}
            except ObjectDoesNotExist:
                energia_resultado = {'error': 'Erro: Tipo de energia não encontrado.'}
        
        # Cálculo de ônibus
        if km_por_mes_onibus:
            try:
                km_por_mes_onibus = float(km_por_mes_onibus)
                if km_por_mes_onibus < 0:
                    raise ValueError('Km por mês não pode ser negativo.')
                carro_obj = Carro.objects.get(tipo='Ônibus')
                credito, anual = onibus(km_por_mes_onibus, carro_obj)
                if credito > 0:
                    onibus_resultado = {'credito': round(credito, 3), 'anual': round(anual, 3)}
                else:
                    onibus_resultado = None
                request.session['onibus_resultado'] = onibus_resultado
            except ValueError as e:
                return HttpResponse(str(e), status=400)
            except ObjectDoesNotExist:
                onibus_resultado = {'error': 'Erro: Tipo de ônibus não encontrado.'}
        
        # Cálculo de gás
        if gas_tipo:
            try:
                gas_obj = Gas.objects.get(modo_de_calculo=gas_tipo)
                if gas_tipo == 'Botijão (13kg)' and botijao_gas:
                    botijao_gas = float(botijao_gas)
                    if botijao_gas < 0:
                        raise ValueError('Botijão de gás não pode ser negativo.')
                    credito, anual = gas_botijao(botijao_gas, gas_obj)
                    if credito > 0:
                        gas_resultado = {'credito': round(credito, 3), 'anual': round(anual, 3)}
                    else:
                        gas_resultado = None
                    request.session['gas_resultado'] = gas_resultado
                elif gas_tipo == 'Gás Encanado (m³/mês)' and volume_gas:
                    volume_gas = float(volume_gas)
                    if volume_gas < 0:
                        raise ValueError('Volume de gás não pode ser negativo.')
                    credito, anual = gas_encanado(volume_gas, gas_obj)
                    if credito > 0:
                        gas_resultado = {'credito': round(credito, 3), 'anual': round(anual, 3)}
                    else:
                        gas_resultado = None
                    request.session['gas_resultado'] = gas_resultado
                else:
                    gas_resultado = {'error': 'Erro: Nenhum valor válido foi fornecido para o cálculo de gás.'}
            except ObjectDoesNotExist:
                gas_resultado = {'error': 'Erro: Tipo de gás não encontrado.'}

    # Soma dos valores, individualmente
    if carro_resultado and 'anual' in carro_resultado:
        total_anual += carro_resultado['anual']
    if energia_resultado and 'anual' in energia_resultado:
        total_anual += energia_resultado['anual']
    if onibus_resultado and 'anual' in onibus_resultado:
        total_anual += onibus_resultado['anual']
    if gas_resultado and 'anual' in gas_resultado:
        total_anual += gas_resultado['anual']

    # Caso ao menos 1 dos cálculos acima forem realizados, retornar valores abaixo
    if total_anual > 0:        
        arvores_necessarias, custo_arvores = arvores(total_anual)
        arvores_necessarias = ceil(arvores_necessarias)
        valor_tonelada = round(valor_da_tonelada(total_anual), 2)

    # Retorno para renderização no site
    return render(request, 'carbono/calculadora.html', {
        'carro_resultado': carro_resultado,
        'energia_resultado': energia_resultado,
        'onibus_resultado': onibus_resultado,
        'gas_resultado': gas_resultado,
        'total_anual': round(total_anual, 3),
        'arvores_necessarias': arvores_necessarias,
        'custo_arvores': round(custo_arvores, 2),
        'valor_tonelada': valor_tonelada,
        'carros': carros,
        'energias': energias,
        'onibus': onibus,
        'gases': gases,
    })


'''
******************* FUNÇÕES PARA LIMPAR OS RESULTADOS DOS CÁLCULOS, INDIVIDUALMENTE OU TODOS JUNTOS *******************
'''

def limpar_carro(request):
    request.session['carro_resultado'] = None
    return redirect('calculadora')

def limpar_energia(request):
    request.session['energia_resultado'] = None
    return redirect('calculadora')

def limpar_onibus(request):
    request.session['onibus_resultado'] = None
    return redirect('calculadora')

def limpar_gas(request):
    request.session['gas_resultado'] = None
    return redirect('calculadora')
    
def limpar_sessao(request):
    request.session['carro_resultado'] = None
    request.session['energia_resultado'] = None
    request.session['onibus_resultado'] = None
    request.session['gas_resultado'] = None
    return redirect('calculadora')
