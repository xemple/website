# -*- coding: utf-8 -*-
import os
import datetime
from django.conf import settings
from django.db import transaction
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from apps.billing.models import Subscription, Transaction, Invoice



# PREPARER SWITCHING POUR HTTPS
@login_required
@transaction.commit_on_success
def manager_panel(request):
	user=request.user
	pending_transactions = Transaction.objects.select_related().filter(invoice__user=user.id, invoice__is_paid=False)
	for t in pending_transactions:
		invoice_item =  t.invoice.get_item()
	return render_to_response('manager/manager_panel.html', {'pending_transactions':pending_transactions, 'invoice_item':invoice_item}, context_instance=RequestContext(request))
	
@login_required	
def manager_dashboard(request):
	my_subs = Subscription.objects.filter(user=request.user)
	return render_to_response('manager/manager_dashboard.html', {'my_subs':my_subs}, context_instance=RequestContext(request))
@login_required
def manager_tdashboard(request):
	return render_to_response('manager/dashboard.html', {}, context_instance=RequestContext(request))
@login_required	
def manager_tadmin(request):
	return render_to_response('manager/admin.html', {}, context_instance=RequestContext(request))
@login_required	
def manager_tpanel(request):
	return render_to_response('manager/panel.html', {}, context_instance=RequestContext(request))
	
@login_required
def accounting_invoices(request):
	invoices = Invoice.objects.filter(user=request.user)
	return render_to_response('manager/accounting_invoices.html', {'invoices':invoices}, context_instance=RequestContext(request))
	
@login_required
def accounting_invoice_details(request, invoice_id):
	invoice = Invoice.objects.get(id=invoice_id)
	return render_to_response('manager/accounting_invoice_details.html', {'invoice':invoice}, context_instance=RequestContext(request))