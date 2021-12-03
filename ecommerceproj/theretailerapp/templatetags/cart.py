from django import template
register = template.Library()

@register.filter(name='cart_quantity')
def cart_quantity(product, cart):
    keys = cart.keys()
    for id in keys:
        if id == str(product.id):
            return cart.get(id)
    return 0
