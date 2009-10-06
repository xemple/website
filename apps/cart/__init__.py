# -*- coding: utf-8 -*-
def get_cart(request):
    from apps.cart.models import Cart
    try:
        cart = request.session['cart']
    except KeyError:
        cart = Cart()
        request.session['cart'] = cart
    return cart