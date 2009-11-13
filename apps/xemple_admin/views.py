# -*- coding: utf-8 -*-
import os
import datetime
from django.conf import settings
from django.db import transaction
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from apps.support.models import Ticket, Message, Knowledge
from apps.xemple_admin.forms import MessageForm, TicketForm, KnowledgeForm



@permission_required('is_staff')
def index(request):
	return render_to_response('xemple_admin/index.html', {}, context_instance=RequestContext(request))
	
@permission_required('is_staff')
def staff_index(request):
	return render_to_response('xemple_admin/staff.html', {}, context_instance=RequestContext(request))
	
@permission_required('is_staff')
def staff_tickets_index(request):
	new_tickets = Ticket.objects.filter(answered=False).exclude(status=2)
	pending_tickets = Ticket.objects.filter(status=1)
	return render_to_response('xemple_admin/support/staff_tickets_index.html', {'new_tickets':new_tickets, 'pending_tickets':pending_tickets}, context_instance=RequestContext(request))
	
@permission_required('is_staff')
def staff_ticket_answer(request, ticket_id):
	ticket = Ticket.objects.get(id=ticket_id)
	messages = ticket.ticket_messages.filter().order_by('-created_at')
	message_instance = Message()
	ticket_instance = ticket
	if request.method == "POST":
		message_form = MessageForm(request.POST, request.FILES, instance=message_instance)
		ticket_form = TicketForm(request.POST, instance=ticket_instance)
		if ticket_form.is_valid():
			ticket_form.save()
		if message_form.is_valid():
			new_message = message_form.save(commit=False)
			new_message.user, new_message.ticket = request.user, ticket
			new_message.save()
			return HttpResponseRedirect(reverse('staff_ticket_answer', args=[ticket_id]))
	message_form = MessageForm(instance=message_instance)
	ticket_form = TicketForm(instance=ticket_instance)
	return render_to_response('xemple_admin/support/staff_ticket_answer.html', {'ticket':ticket, 'messages':messages, 'message_form':message_form, 'ticket_form':ticket_form}, context_instance=RequestContext(request))