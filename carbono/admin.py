from django.contrib import admin

from .models import Carro, Energia

class CarrosAdmin(admin.ModelAdmin):
    ordering = ('id',)
    list_display = ('id', 'tipo', 'legenda', 'emissao', 'consumo')
    list_display_links = ('tipo',)
    search_fields = ('tipo', 'consumo')
    list_filter = ('tipo', 'emissao')
    list_per_page = 5

admin.site.register(Carro, CarrosAdmin)

class EnergiaAdmin(admin.ModelAdmin):
    ordering = ('id',)
    list_display = ('id', 'modo_de_calculo', 'legenda', 'emissao')
    list_display_links = ('modo_de_calculo',)
    
admin.site.register(Energia, EnergiaAdmin)
