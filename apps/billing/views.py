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
from apps.client.models import Client, Contact
from apps.billing.models import Offer, Subscription
from apps.service.models import Service
from apps.testservers.dnserver import check_avail_dn_ext
from apps.cart.models import Cart


@login_required 
def create_subscription_from_cart(client, cart, service=False):

	###########
	if service == False:
		new_service = Service.objects.create_new_service(client=client, name="oLOLOLOL")
	##########
	
	for item in cart.items():
		offer = Offer.objects.get(id=item.sku)
		qt = item.units
		created_obj = Subscription.objects.create_subscription(offer=offer, quantity = qt, service = new_service.id)
	return True
	
	
@login_required
def select_offer(request):
	cart = request.cart
	cart._items = {}
	offers = Offer.objects.filter(is_hosting=True)
	return render_to_response('billing/select_offer.html', {'offers':offers}, context_instance=RequestContext(request))
	
	
def select_options(request, offer_id):
	cart = request.cart
	offers = Offer.objects.filter(offer=int(offer_id))
	return render_to_response('billing/select_options.html', {'offers':offers}, context_instance=RequestContext(request))
	
	
	
def domain_choice(request):
	if request.POST:
		domain = request.POST['domain']
		return HttpResponseRedirect(reverse('dn_check_domain', args=(str(domain),)))
	return render_to_response('billing/domain_choice.html', {}, context_instance=RequestContext(request))
	
def dn_check_domain(request, check_domain): 
	domain, res_dict = check_avail_dn_ext(str(check_domain))
	dn_offers = Offer.objects.filter(domain_ext__in=res_dict)
	if request.POST:
		checked_offers = request.POST.getlist('offer')
		cart = request.cart
		for o in checked_offers:
			cart.add_item(int(o))
		print 'ok'
		print cart.items()
		return HttpResponseRedirect(reverse('cart_update'))
	return render_to_response('billing/domain_check.html', {'domain':domain, 'res_dict':res_dict, 'dn_offers':dn_offers}, context_instance=RequestContext(request))
	
	