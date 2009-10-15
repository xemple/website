# -*- coding: utf-8 -*-
import datetime
from django.conf import settings
from django.db import transaction
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from apps.billing.models import Offer, MiniCart, Invoice, Subscription, InvoiceItem, Transaction
from apps.resources.tools import calculate_billing
from apps.billing.forms import VerifyInvoiceCheck




#### PAGES


def temporary_offers_page(request):
	return render_to_response('billing/temporary_offers_page.html', {}, context_instance=RequestContext(request))

#1
@login_required
def select_offer(request):
	offers = Offer.objects.filter(is_active=True, is_public=True)
	return render_to_response('billing/select_offer.html', {'offer_list':offers}, context_instance=RequestContext(request))
	
#2	
@login_required	
def select_details(request, offer_id):
	offer = Offer.objects.get(id=int(offer_id))
	return render_to_response('billing/select_details.html', {'offer':offer}, context_instance=RequestContext(request))
	
#3
@login_required
def verify_invoice(request):
	user=request.user
	try:
		request.session['mycart']
	except KeyError:
		return HttpResponseRedirect(reverse('manager_panel'))
	selection = request.session['mycart']
	offer = Offer.objects.get(id=int(selection.item_id))
	quantity = selection.quantity
	offer_price, quantity, total_wot, vat_rate, vat, total_ti =  calculate_billing(user, offer, quantity)
	if request.method == 'POST':
		form = VerifyInvoiceCheck(request.POST)
		if form.is_valid():
			invoice = Invoice.objects.generate_invoice(user, vat_rate)
			subscription = Subscription.objects.create_new_subscription(selection.item_id, user.id)
			invoice_item = InvoiceItem.objects.create_invoice_item(subscription.id, invoice.id, selection.item_id, quantity)
			transaction = Transaction.objects.new_transaction(invoice.id, total_ti)
			del request.session['mycart']
			return HttpResponseRedirect(reverse('pay_invoice', args=[invoice.id,]))
	form = VerifyInvoiceCheck()
	return render_to_response('billing/verify_invoice.html', {	'offer_price':offer_price, 'quantity':quantity, 
																'total_wot':total_wot, 'vat_rate':vat_rate, 
																'vat':vat, 'total_ti':total_ti, 'offer':offer, 'user':user, 'form':form }, 
																context_instance=RequestContext(request))
											
											
#4
@login_required			
def pay_invoice(request, invoice_id):
	transaction = Invoice.objects.get(id=invoice_id).get_last_transaction()
	print transaction
	return render_to_response('billing/pay_invoice.html', {'transaction':transaction}, context_instance=RequestContext(request))
	
@login_required
def user_bank_return(request, transaction_id):
	transaction = Transaction.objects.get(id=transaction_id)
	if transaction.frozen == False and transaction.invoice.is_paid == True:
		answer = True
	else:
		answer = False
	return render_to_response('billing/user_bank_return.html', {'answer':answer}, context_instance=RequestContext(request))
		

#### OPERATIONS

def create_minicart_item(request, item_id, quantity):
	redirect_url = reverse('select_offer')
	request.session['mycart'] = MiniCart(item_id=int(item_id), quantity=int(quantity))
	if request.POST:
		redirect_url = request.POST.get('back', redirect_url)
	return HttpResponseRedirect(redirect_url)
