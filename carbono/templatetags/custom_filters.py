from django import template

'''
FORMATAÇÃO DE NÚMEROS DAS TEMPLATES PARA PONTUAR NÚMEROS A CADA 3 DÍGITOS E PERMITIR FORMATAÇÃO PARA NÚMEROS APÓS DA VÍRGULA
'''

# Registro para os filtros personalizados
register = template.Library()

# Registro da função format_number para ser resgatada no template
@register.filter

# Converte o valor para float, formata a string de acordo com as casas decimais e retorna o valor personalizado, dando abertura para selecionar quando dígitos pode vir depois da vírgula (padrão é 3)
def format_number(value, decimal_places=3):
    try:
        value = float(value)
        format_string = f"{{value:,.{decimal_places}f}}"
        formatted_value = format_string.format(value=value)
        return formatted_value.replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return value
