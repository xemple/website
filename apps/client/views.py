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
from apps.client.forms import ClientForm, NewClientForm


@transaction.commit_on_success
def client_new(request):
	model_instance = Client()
	if request.POST:
		form = NewClientForm(data=request.POST, instance=model_instance)
		if form.is_valid():
			client, username, password  = form.save()
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect(reverse('select_offer'))
			return HttpResponseRedirect(reverse('select_offer'))
	else:
		form = NewClientForm(instance=model_instance)
	return render_to_response('client/client_form.html', {'form':form}, context_instance=RequestContext(request))