# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('apps.billing.views',
    url(r'^$','temporary_offers_page', name='temporary_offers_page'),
	url(r'^select_offer/$','select_offer', name='select_offer'),
	url(r'^select_details/(?P<offer_id>\d+)/$','select_details', name='select_details'),
	url(r'^verify_invoice/$','verify_invoice', name='verify_invoice'),
	url(r'^create_minicart_item/item=(\d+)/qt=(\d+)/$', 'create_minicart_item', name='create_minicart_item'),

)