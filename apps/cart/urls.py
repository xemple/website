# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from django.utils.translation import ugettext as _
	
urlpatterns = patterns('apps.cart.views',

    url(r'^$', 'cart', name="cart"),
    url(r'^add/(?P<product_code>\w+)/$', 'add_item', name='cart_add_item'),
    url(r'^remove/(?P<product_code>\w+)/$', 'remove_item',  name='cart_remove_item'),
    url(r'^update/$', 'update_cart', name='cart_update'),
    url(r'^checkout/$', 'checkout', name='cart_checkout'),
)
