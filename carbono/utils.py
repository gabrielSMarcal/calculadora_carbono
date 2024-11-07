from math import ceil

'''
**********************************************
* FUNÇÕES DAS CALCULADORAS (RESULTADO FINAL) *
**********************************************
'''

# Função para cálculo do valor do CC futuro baseado na TCO2
def valor_da_tonelada(co, MEDIA_CC, MEDIA_EURO):
    media_valor_credito = (MEDIA_CC * MEDIA_EURO)  # Média dos últimos 12 meses
    
    valor = co * media_valor_credito
    return valor

# Função para cálculo de índice de árvores necessárias para compensar, baseado na TCO2
def arvores(co, CUSTO_POR_ARVORE, ABSORCAO):
        
    arvore = co / ABSORCAO
    custo = ceil(arvore) * CUSTO_POR_ARVORE 
    return (arvore, custo)

'''
***********************************************************************************************
* FUNÇÕES PARA CÁLCULO DE CARBONO, RETORNANDO SEMPRE O VALOR MENSAL (credito) E ANUAL (anual) *
***********************************************************************************************
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
def energia_reais(valor_da_conta, energia_obj, CONV_ENERGIA):
    valor_da_conta = float(valor_da_conta)
    conversao = valor_da_conta / CONV_ENERGIA
    emissao = conversao * energia_obj.emissao
    credito = emissao / 1000
    anual = credito * 12
    
    return (credito, anual)

# Função para calcular carbono de ônibus, baseado na quilometragem mensal usada pelo usuário, dividido por uma média de passageiros.
def onibus(km_por_mes_onibus, carro_obj, MEDIA_PASSAGEIROS):
    km_por_mes_onibus = float(km_por_mes_onibus)
    emissao = (km_por_mes_onibus / carro_obj.consumo) * carro_obj.emissao / MEDIA_PASSAGEIROS  # Média de 40 passageiros por ônibus
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