# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('apps.billing.views',
    url(r'^$','temporary_offers_page', name='temporary_offers_page'),
	url(r'^select_offer/$','select_offer', name='select_offer'),
	url(r'^select_details/(?P<offer_id>\d+)/$','select_details', name='select_details'),
	url(r'^verify_invoice/$','verify_invoice', name='verify_invoice'),
	url(r'^pay_invoice/invoice=(?P<invoice_id>\d+)/$','pay_invoice', name='pay_invoice'),
	url(r'^create_minicart_item/item=(\d+)/qt=(\d+)/$', 'create_minicart_item', name='create_minicart_item'),
	url(r'^user_bank_return/transaction=(?P<transaction_id>\d+)/$','user_bank_return', name='user_bank_return'),
	url(r'^bank_return/trans=(?P<trans_num>\d+)/status=(?P<status>\w+)/$', 'temporary_bank_return_validator', name='temporary_bank_return_validator'),
	url(r'^renew/$','renew_duration_choice', name='renew_duration_choice'),

)