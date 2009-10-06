# -*- coding: utf-8 -*-
import re

from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response as render
from django.http import HttpResponse, HttpResponseRedirect
from django import template
from apps.billing.views import create_subscription_from_cart
from apps.billing.models import Quote, QuoteItem
from apps.client.models import Client
from django.contrib.auth.decorators import login_required
#################
from apps.testservers.cmut_testserver import pay
#################


from apps.cart.models import Cart
from apps.cart.decorators import cookie_required



@login_required
@cookie_required	
def add_item(request, product_code): 
	redirect_url = reverse('cart')
	quantity = 0
	if request.POST:
		redirect_url = request.POST.get('back', redirect_url)
		try:
			quantity = int(request.POST.get('quantity', 1))
		except ValueError:
			quantity = 0
	elif request.GET:
		redirect_url = request.GET.get('back', redirect_url)
		try:
			quantity = int(request.GET.get('q', 1))
		except ValueError:
			quantity = 0
	
	if quantity > 0:
		cart = request.cart
		if quantity == 1:
			cart.add_item(product_code)
		else:
			cart.inc_item_count(product_code, quantity)
		request.session['cart'] = cart
	
	return HttpResponseRedirect(redirect_url)
	
@login_required
@cookie_required
def remove_item(request, product_code):
	redirect_url = reverse('cart')
	if request.POST:
		redirect_url = request.POST.get('back', redirect_url)
	elif request.GET:
		redirect_url = request.GET.get('back', redirect_url)
	
	cart = request.cart
	cart.remove_item(product_code)
	request.session['cart'] = cart 
	return HttpResponseRedirect(redirect_url)
	
@login_required	
@cookie_required
def update_cart(request):
	redirect_url = reverse('cart')
	if request.POST:
		cart = request.cart
		do_empty = request.POST.get('do_empty', False)
		do_checkout = request.POST.get('do_checkout', False)
		if do_empty:
			cart.empty()
		else:
			for key, value in request.POST.items():
				if key.startswith('count_'):
					try:
						cart.update_item(key[6:], int(value))
					except ValueError:
						continue
		request.session['cart'] = cart
		if do_checkout:
			redirect_url = reverse('cart_checkout')
		else:
			redirect_url = request.POST.get('back', redirect_url)
	return HttpResponseRedirect(redirect_url)

@login_required
@cookie_required  
def cart(request):
	cart = request.cart
	return render('cart/cart.html', {
		'cart': cart,
		'redirect_url': request.path,
	}, context_instance=template.RequestContext(request))

@login_required
@cookie_required	  
def checkout(request):
	cart = request.cart
	if request.method == 'POST':
		client=Client.objects.get(id=request.user.id)
		quote = Quote.objects.create_new_quote(client)
		
		create_subscription_from_cart(client = client, cart=cart, service=False)
		result, amount, unique_id = pay(cart.get_total_price)
		if result == True:
			print 'paid'
	return render('cart/checkout.html', {'cart': cart}, context_instance=template.RequestContext(request))
	
	
	
	
	
	