from django import template


register = template.Library()


@register.filter(name="calculate_total")
def calculate_total(selling_price, quantity):
    return selling_price * quantity

