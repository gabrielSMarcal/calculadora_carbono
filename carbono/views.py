from django.shortcuts import render

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

# Função de cálculo para carros
def carro(km_por_mes_str, carro_id):
    km_por_mes = float(km_por_mes_str)
    
    try:
        carro_obj = Carro.objects.get(pk=carro_id)
        consumo = km_por_mes / carro_obj.consumo
        emissao = consumo * carro_obj.emissao
        credito = emissao / 1000
        anual = credito * 12
        
        return (credito, anual)
    except (ZeroDivisionError, Carro.DoesNotExist) as e:
        print(f'Erro no cálculo: {e}')
        return None
    
# Função de cálculo para energia por Kwh
def energia_kwh(kwh_usado):
    kwh_usado = float(kwh_usado)
    
    emissao = kwh_usado * Energia.emissao
    credito = emissao / 1000
    anual = credito * 12
    
    return (credito, anual)

# Função de cálculo para energia por conta de luz
def energia_reais(valor_da_conta):

    conversao = valor_da_conta / 0.37
    emissao = conversao * Energia.emissao
    credito = emissao / 1000
    anual = credito * 12
    
    return(credito, anual)
    
# Renderização do site
def teste(request):
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
                carro_obj = Carro.objects.get(tipo=carro_tipo)
                credito, anual = carro(km_por_mes, carro_obj.pk)
                carro_resultado = {'credito': credito, 'anual': anual}
            except Carro.DoesNotExist:
                carro_resultado = {'error': f'Carro {carro_tipo} não encontrado.'}
            except (ValueError, AttributeError) as e:
                print(f"Erro no cálculo do carro: {e}")

        if 'energia_tipo' in request.POST:
            energia_tipo = request.POST['energia_tipo']
            if energia_tipo == 'kwh':
                kwh_usado = request.POST.get('kwh_usado')
                if kwh_usado:
                    try:
                        credito, anual = energia_kwh(kwh_usado)
                        energia_resultado = {'credito': credito, 'anual': anual}
                    except (ValueError, AttributeError) as e:
                        print(f"Error in energia_kwh calculation: {e}")
            elif energia_tipo == 'conta':
                valor_da_conta = request.POST.get('valor_da_conta')
                if valor_da_conta:
                    try:
                        credito, anual = energia_reais(valor_da_conta)
                        energia_resultado = {'credito': credito, 'anual': anual}
                    except (ValueError, AttributeError) as e:
                        print(f"Error in energia_reais calculation: {e}")

        if carro_resultado and energia_resultado:
            total_anual = carro_resultado['anual'] + energia_resultado['anual']
            arvores_necessarias = arvores(total_anual)
            valor_tonelada = valor_da_tonelada(total_anual)
            
    return render(request, 'carbono/teste.html', {
        'carro_resultado': carro_resultado,
        'energia_resultado': energia_resultado,
        'total_anual': total_anual,
        'arvores_necessarias': arvores_necessarias,
        'valor_tonelada': valor_tonelada
    })