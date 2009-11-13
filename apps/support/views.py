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
from apps.support.models import Ticket, Message, Knowledge
from apps.support.forms import MessageForm, TicketForm, NewKnowledgeForm

@login_required
def support_index(request):
	return render_to_response('support/support.html', {}, context_instance=RequestContext(request))
	
@login_required
def knowledge_db(request):
	knowledges = Knowledge.objects.filter(is_active=True)
	return render_to_response('support/knowledge_database.html', {'knowledges':knowledges}, context_instance=RequestContext(request))
	
@login_required
def knowledge_details(request, know_id):
	knowledge = Knowledge.objects.get(id=know_id)
	return render_to_response('support/knowledge_details.html', {'knowledge':knowledge}, context_instance=RequestContext(request))
	
@login_required
def knowledge_contribution(request):
	knowledge = Knowledge()
	if request.method == 'POST':
		form = NewKnowledgeForm(request.POST, instance = knowledge)
		if form.is_valid():
			new_knowledge = form.save(commit=False)
			new_knowledge.user = request.user
			new_knowledge.save()
			return HttpResponseRedirect(reverse('knowledge_contribution_thanks'))
	form = NewKnowledgeForm(instance=knowledge)
	return render_to_response('support/knowledge_contribution.html', {'form':form}, context_instance=RequestContext(request))
	
@login_required
def knowledge_contribution_thanks(request):
	return render_to_response('support/knowledge_contribution_thanks.html', {}, context_instance=RequestContext(request))	

@login_required
def mytickets(request):
	awaiting_answer_tickets = Ticket.objects.filter(user = request.user, answered=0).exclude(status=2).order_by('-created_at')
	answered_tickets = Ticket.objects.filter(user = request.user, status=0 or 1, answered=1).exclude(status=2).order_by('-created_at')
	return render_to_response('support/mytickets.html', {'awaiting_answer_tickets':awaiting_answer_tickets, 'answered_tickets':answered_tickets}, context_instance=RequestContext(request))
	
	
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
		