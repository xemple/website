def get_cart(request):
    from apps.billing.models import MyCart
    try:
        cart = request.session['cart']
    except KeyError:
        cart = MyCart()
        request.session['cart'] = cart
    return cart