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
from apps.billing.models import Offer, MiniCart




#### PAGES

def temporary_offers_page(request):
	return render_to_response('billing/temporary_offers_page.html', {}, context_instance=RequestContext(request))


@login_required
def select_offer(request):
	offers = Offer.objects.filter(is_active=True, is_public=True)
	return render_to_response('billing/select_offer.html', {'offer_list':offers}, context_instance=RequestContext(request))
	
	
def select_details(request, offer_id):
	offer = Offer.objects.get(id=int(offer_id))
	return render_to_response('billing/select_details.html', {'offer':offer}, context_instance=RequestContext(request))

	
def verify_invoice(request):
	selection = request.session['mycart']
	offer = Offer.objects.get(id=int(selection.item_id))
	quantity = selection.quantity
	print offer
	print quantity
	return render_to_response('billing/verify_invoice.html', {}, context_instance=RequestContext(request))
	
	
#### OPERATIONS

def create_minicart_item(request, item_id, quantity):
	redirect_url = reverse('select_offer')
	request.session['mycart'] = MiniCart(item_id=int(item_id), quantity=int(quantity))
	if request.POST:
		redirect_url = request.POST.get('back', redirect_url)
	return HttpResponseRedirect(redirect_url)
