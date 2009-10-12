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
from apps.billing.models import Offer, MiniCart, Invoice
from apps.resources.tools import calculate_billing




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
	selection = request.session['mycart']
	offer = Offer.objects.get(id=int(selection.item_id))
	quantity = selection.quantity
	offer_price, quantity, total_wot, vat_rate, vat, total_ti =  calculate_billing(user, offer, quantity)
	print "___________________"
	print ''
	print "Price : %s Euros" % offer_price
	print "Quantity : %s" % quantity
	print "Total w/o Taxes : %s Euros" % total_wot
	print "VAT Rate : %s" % vat_rate
	print "VAT : %s Euros" % vat
	print "Total with Taxes : %s Euros" % total_ti
	print ''
	print "___________________"
	invoice = Invoice.objects.generate_invoice(user)
	
	# IMPORTANT : Modifications-check #######
	if request.method == 'POST':
		print "prout"
		actual_user = request.user
		if request.session['user_check'] == actual_user:
			print " USER HAS SAME INFORMATIONS"
		else:
			print " USER CHANGED INFORMATIONS"
	#########################################
			
	return render_to_response('billing/verify_invoice.html', {	'offer_price':offer_price, 'quantity':quantity, 
																'total_wot':total_wot, 'vat_rate':vat_rate, 
																'vat':vat, 'total_ti':total_ti, 'offer':offer }, 
																context_instance=RequestContext(request))
	
#4
@login_required			
def paiment_exit(request):
	return render_to_response('billing/paiment_exit.html', {}, context_instance=RequestContext(request))
	
	
	
#### OPERATIONS

def create_minicart_item(request, item_id, quantity):
	redirect_url = reverse('select_offer')
	request.session['mycart'] = MiniCart(item_id=int(item_id), quantity=int(quantity))
	if request.POST:
		redirect_url = request.POST.get('back', redirect_url)
	return HttpResponseRedirect(redirect_url)
