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
from django.contrib.auth import REDIRECT_FIELD_NAME


def myaccount(request):

	return render_to_response('client/my_account.html', {}, context_instance=RequestContext(request))
	
	
	
def client_new(request):
	redirect_to = request.REQUEST.get('next', '')
	if request.POST.has_key('register'):
		form = NewClientForm(request.POST)
		if form.is_valid():
			username, password = form.save()
			print "USERNAME : %s" % username
			print "PASSWORD : %s" % password
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					if redirect_to == '':
						return HttpResponseRedirect(reverse('manager_panel'))
					else:
						return HttpResponseRedirect(redirect_to)
			return HttpResponseRedirect(reverse('client_new'))
	else:
		form = NewClientForm()
	return render_to_response('client/client_form.html', {'form':form, 'next':redirect_to}, context_instance=RequestContext(request))