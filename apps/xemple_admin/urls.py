# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.utils.translation import ugettext as _



urlpatterns = patterns('apps.xemple_admin.views',
	url(r'^$', 'index', name='xadmin_index'),
	url(r'^staff/$', 'staff_index', name='xadmin_staff_index'),
	url(r'^staff/tickets/$', 'staff_tickets_index', name='staff_tickets_index'),
	url(r'^staff/tickets/(?P<ticket_id>\d+)/answer/$','staff_ticket_answer', name='staff_ticket_answer'),
	
	
)


### DEV MEMOS ###
"""
url(r'^$', 'manager_panel', name='manager_panel'),
url(r'^dashboard/', 'manager_dashboard', name='manager_dashboard'),
url(r'^accounting/invoice/details=(?P<invoice_id>\d+)/$', 'accounting_invoice_details', name='accounting_invoice_details'),
"""