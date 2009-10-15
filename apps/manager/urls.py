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
	url(r'^register/$','apps.client.views.client_new', name='client_new'),

)