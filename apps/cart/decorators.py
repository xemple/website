# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response as render
from django.template import RequestContext, loader, Context

__all__ = ['cookie_required']

def cookie_required(f):
    def _decorated(request, *args, **kwargs):
        if not request.session.test_cookie_worked():
            return render_to_response(
                'shop/nocookies.html',
                context_instance=template.RequestContext(request)
            )
        request.session.delete_test_cookie()
        return f(request, *args, **kwargs)
    return _decorated