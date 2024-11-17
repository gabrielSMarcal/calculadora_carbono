from django.db import models
from django.db.models.base import class_prepared

'''
*********************************************************************************************************************
* PARTE DO CODIGO ONDE FICA CONFIGURADO O MODELO PARA CADA POSSÍVEL TIPO DE CÁLCULO QUE SERÁ APLICADO.              *
* NOTA QUE ÔNIBUS ESTÁ CONFIGURADO DENTRO DO CARRO, POR TER ESTRUTURA SEMELHANTE, MAS REALIZA UM CÁLCULO DIFERENTE. *
*********************************************************************************************************************
'''

# Classe que configura o modelo para Carros
class Carro(models.Model):
    tipo = models.CharField(max_length=100, null=False, blank=False)
    legenda = models.CharField(max_length=255, null=False, blank=False)
    consumo = models.FloatField(null=False, blank=False)
    emissao = models.FloatField(null=False, blank=False)

    # Definição do título para cada tipo de Carro
    def __str__(self):
        return f'Tipo de cálculo: {self.tipo}'

# Classe que configura o modelo para Energia
class Energia(models.Model):
    modo_de_calculo = models.CharField(max_length=100, null=False, blank=False)
    legenda = models.CharField(max_length=100, null=False, blank=False)
    emissao = models.FloatField(null=False, blank=False)

    # Definição do título para cada modo de cálculo de Energia
    def __str__(self):
        return f'Modo de cálculo : {self.modo_de_calculo}'

# Classe que configura o modelo para Gás
class Gas(models.Model):
    modo_de_calculo = models.CharField(max_length=100, null=False, blank=False)
    legenda = models.CharField(max_length=100, null=False, blank=False)
    emissao = models.FloatField(null=False, blank=False)

    # Definição do título para cada modo de cálculo de Gás
    def __str__(self):
        return f'Modo de cálculo: {self.modo_de_calculo}'

    # Classe para evitar erro na nomenclatura no /admin
    class Meta:
        verbose_name_plural = 'Gás'
