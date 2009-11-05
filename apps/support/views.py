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
from apps.support.models import Ticket, Message
from apps.support.forms import MessageForm, TicketForm

@login_required
def mytickets(request):
	tickets = Ticket.objects.filter(user = request.user).order_by('-created_at')
	return render_to_response('support/mytickets.html', {'tickets':tickets}, context_instance=RequestContext(request))
	
	
@login_required
def ticket_details(request, ticket_id):
	ticket = Ticket.objects.get(id=ticket_id)
	if ticket.user.id is not request.user.id:
		return HttpResponseRedirect(reverse('manager_panel'))
	messages = ticket.ticket_messages.filter().order_by('-created_at')
	return render_to_response('support/ticket_details.html', {'ticket':ticket, 'messages':messages}, context_instance=RequestContext(request))
	

@login_required
def answer_ticket(request, ticket_id, template_name='support/answer_ticket.html'):
	redirect_url = request.META['HTTP_REFERER']
	ticket = Ticket.objects.get(id=ticket_id)
	if request.user.has_perm('is_staff'):
		pass
	else:
		if ticket.user.id is not request.user.id or ticket.status==2:
			return HttpResponseRedirect(redirect_url)
	model_instance = Message()
	if request.method == "POST":
		form = MessageForm(request.POST, request.FILES, instance=model_instance)
		if form.is_valid():
			new_message = form.save(commit=False)
			new_message.user = request.user
			new_message.ticket = ticket
			new_message.save()
			return HttpResponseRedirect(reverse('ticket_details', args=[ticket_id]))
	form = MessageForm(instance=model_instance)
	return render_to_response(template_name, {'form':form, 'redirect_url':redirect_url}, context_instance=RequestContext(request))
	
	
@login_required
def new_ticket(request):
	ticket_instance = Ticket()
	message_instance = Message()
	if request.method == "POST":
		ticket_form = TicketForm(request.POST, instance=ticket_instance)
		message_form = MessageForm(request.POST, request.FILES, instance=message_instance)
		if ticket_form.is_valid() and message_form.is_valid():
			new_ticket = ticket_form.save(commit=False)
			new_ticket.user = request.user
			new_ticket.save()
			new_message = message_form.save(commit=False)
			new_message.user, new_message.ticket = request.user, new_ticket
			new_message.save()
			return HttpResponseRedirect(reverse('ticket_details', args=[new_ticket.id]))
	ticket_form = TicketForm(instance=ticket_instance)
	message_form = MessageForm(instance=message_instance)
	return render_to_response('support/new_ticket.html', {'ticket_form':ticket_form, 'message_form':message_form}, context_instance=RequestContext(request))
	
	
@login_required
def quick_ticket_answer(request, ticket_id):
	print 'caca'
	if request.method == "SEND":
		new_message = Message.objects.create(user=request.user, ticket=ticket_id, content=request.POST['Message'])
		new_message.save()
		redirect_url = request.META['HTTP_REFERER']
		redirect_url = request.POST.get('back', redirect_url)
	return HttpResponseRedirect(redirect_url)
		