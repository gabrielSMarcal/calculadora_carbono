from django import template

register = template.Library()

@register.filter
def format_number(value, decimal_places=3):
    try:
        value = float(value)
        format_string = f"{{value:,.{decimal_places}f}}"
        formatted_value = format_string.format(value=value)
        return formatted_value.replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return value