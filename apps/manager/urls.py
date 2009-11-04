# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.utils.translation import ugettext as _



urlpatterns = patterns('apps.manager.views',
	url(r'^$', 'manager_panel', name='manager_panel'),
	url(r'^dashboard/', 'manager_dashboard', name='manager_dashboard'),
	url(r'^tdashboard/$', 'manager_tdashboard', name='manager_tdashboard'),
	url(r'^tadmin/$', 'manager_tadmin', name='manager_tadmin'),
	url(r'^tpanel/$', 'manager_tpanel', name='manager_tpanel'),		
	url(r'^accounting/invoices/$', 'accounting_invoices', name='accounting_invoices'),	
	url(r'^accounting/invoice/details=(?P<invoice_id>\d+)/$', 'accounting_invoice_details', name='accounting_invoice_details'),	
)


urlpatterns += patterns('',
	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'authentication/login.html'}, name='manager_login'),
	url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'authentication/logout.html'}, name='manager_logout'),

)


urlpatterns += patterns('apps.billing.views',
    url(r'^billing/$','billing_index', name='billing'),
	url(r'^billing/$','temporary_offers_page', name='temporary_offers_page'),
	url(r'^billing/select_offer/$','select_offer', name='select_offer'),
	url(r'^billing/select_details/(?P<offer_id>\d+)/$','select_details', name='select_details'),
	url(r'^billing/verify_invoice/$','verify_invoice', name='verify_invoice'),
	url(r'^billing/pay_invoice/invoice=(?P<invoice_id>\d+)/$','pay_invoice', name='pay_invoice'),
	url(r'^billing/create_minicart_item/item=(\d+)/qt=(\d+)/$', 'create_minicart_item', name='create_minicart_item'),
	url(r'^billing/user_bank_return/transaction=(?P<transaction_id>\d+)/$','user_bank_return', name='user_bank_return'),
	url(r'^billing/bank_return/trans=(?P<trans_num>\d+)/status=(?P<status>\w+)/$', 'temporary_bank_return_validator', name='temporary_bank_return_validator'),
	url(r'^billing/renew/$','renew_duration_choice', name='renew_duration_choice'),

)


urlpatterns += patterns('apps.client.views',
    url(r'^myaccount/$','myaccount', name='myaccount'),
	url(r'^register/$','client_new', name='client_new'),

)

urlpatterns += patterns('apps.support.views',
    url(r'^support/mytickets/$','mytickets', name='mytickets'),
	url(r'^support/ticket/(?P<ticket_id>\d+)/details/$','ticket_details', name='ticket_details'),
	url(r'^support/ticket/(?P<ticket_id>\d+)/answer/$','answer_ticket', name='answer_ticket'),
	url(r'^support/ticket/new/$','new_ticket', name='new_ticket'),

)