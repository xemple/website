# -*- coding: utf-8 -*-
from apps.billing import get_cart

__all__ = ['CartMiddleware']

class CartMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'session'), ""
        request.__class__.cart = get_cart(request)
        request.session.set_test_cookie()
        return None