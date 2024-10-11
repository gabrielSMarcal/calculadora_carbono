from django.db import models

class Carro(models.Model):
    tipo = models.CharField(max_length=100, null=False, blank=False)
    legenda = models.CharField(max_length=255, null=False, blank=False)
    consumo = models.FloatField(null=False, blank=False)
    emissao = models.FloatField(null=False, blank=False)
    
    def __str__(self):
        return f'Tipo de cálculo [tipo={self.tipo}]'

class Energia(models.Model):
    modo_de_calculo = models.CharField(max_length=100, null=False, blank=False)
    legenda = models.CharField(max_length=100, null=False, blank=False)
    emissao = models.FloatField(null=False, blank=False)
    
    def __str__(self):
        return f'Modo de cálculo [modo_de_calculo={self.modo_de_calculo}]'
