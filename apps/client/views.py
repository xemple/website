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
from apps.client.forms import NewClientForm
from apps.client.models import ClientProfile



def client_new(request):
	model_instance = ClientProfile()
	if request.POST:
		form = NewClientForm(request.POST)
		if form.is_valid():
			username, password = form.save()
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect(reverse('manager_dashboard'))
			return HttpResponseRedirect(reverse('client_new'))
	else:
		form = NewClientForm()
	return render_to_response('client/client_form.html', {'form':form}, context_instance=RequestContext(request))