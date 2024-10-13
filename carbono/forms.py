'''from django import forms

from .models import Carro, Energia

class CarroForm(forms.ModelForm):
    tipo = forms.CharField(widget=forms.Select(choices=[
        ('gasolina_1_4', 'Gasolina 1.4'),
        ('gasolina_1_5_2_0', 'Gasolina 1.5 até 2.0'),
        ('gasolina_mais_2_0', 'Gasolina mais de 2.0'),
        ('alcool_1_4', 'Álcool 1.4'),
        ('alcool_1_5_2_0', 'Álcool 1.5 até 2.0'),
        ('alcool_mais_2_0', 'Álcool mais de 2.0'),
        ('gas', 'Gás'),
    ]))

    class Meta:
        model = Carro
        fields = ['tipo', 'consumo', 'emissao']
        widgets = {
            'consumo': forms.NumberInput(attrs={'class': 'form-control'}),
            'emissao': forms.NumberInput(attrs={'class': 'form-control'}),

        }
        
class EnergiaForm(forms.ModelForm):
    tipo_de_calculo = forms.CharField(widget=forms.Select(choices=[
        ('kwh_usado', 'Por Kwh'),
        ('valor_da_conta', 'Por conta de luz')
    ]))
    
    class Meta:
        model = Energia
        fields = ['tipo_de_calculo', 'emissao']
        widgets = {
            'emissao': forms.NumberInput(attrs={'class': 'form-control'})
        }'''