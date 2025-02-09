# myapp/templatetags/custom_filters.py
from django import template

register = template.Library()


@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def sum_total_price(order_items):
    total = 0
    for item in order_items:
        total += item.product.price * item.quantity
    return total
