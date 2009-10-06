# -*- coding: utf-8 -*-
import os
import datetime
from django.conf import settings
from django.db import transaction
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from apps.manager.forms import LoginForm



# PREPARER SWITCHING POUR HTTPS
@transaction.commit_on_success
def manager_login(request, log_class=LoginForm):
	if request.method == 'POST':
		logform =log_class(request.POST)
		if logform.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect(reverse('manager_dashboard', args=[]))			 
	else:

		logform = log_class()
	return render_to_response('manager/authentication/login_form.html', {'logform':logform }, context_instance=RequestContext(request))
	
	
def manager_dashboard(request):
	return render_to_response('manager/manager_dashboard.html', {}, context_instance=RequestContext(request))

def manager_tdashboard(request):
	return render_to_response('manager/dashboard.html', {}, context_instance=RequestContext(request))
	
def manager_tadmin(request):
	return render_to_response('manager/admin.html', {}, context_instance=RequestContext(request))
	
def manager_tpanel(request):
	return render_to_response('manager/panel.html', {}, context_instance=RequestContext(request))