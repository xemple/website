# -*- coding: utf-8 -*-
import datetime
from django.conf import settings
from django.db import transaction
from django.template import RequestContext, Context
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.shortcuts import render_to_response
from apps.client.forms import NewClientForm, UserForm, ProfileForm
from apps.client.models import ClientProfile
from django.contrib.auth import REDIRECT_FIELD_NAME
from apps.emailing.system import xemple_send_mail



def myaccount(request):
	user = User.objects.get(id=request.user.id)
	
	return render_to_response('client/my_account.html', {}, context_instance=RequestContext(request))
	
	
	
def client_new(request, send_mail=True):
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
					infos = '%s // %s' % (username, password)
					if send_mail==True:
						xemple_send_mail('new_user', Context({'user':request.user, 'password':password}))
					if redirect_to == '':
						return HttpResponseRedirect(reverse('manager_panel'))
					else:
						return HttpResponseRedirect(redirect_to)
			return HttpResponseRedirect(reverse('client_new'))
	else:
		form = NewClientForm()
	return render_to_response('client/client_form.html', {'form':form, 'next':redirect_to}, context_instance=RequestContext(request))
	
@login_required 
def edit_client_infos(request):
	user_infos = User.objects.get(id=request.user.id)
	profile_infos = user_infos.get_profile()
	if request.POST.has_key('edit_infos'):
		user_form = UserForm(request.POST, instance=user_infos)
		profile_form = ProfileForm(request.POST, instance=profile_infos)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			return HttpResponseRedirect(reverse('manager_panel'))
	user_form = UserForm(instance=user_infos)
	profile_form = ProfileForm(instance=profile_infos)
	return render_to_response('client/client_edit.html', {'user_form':user_form, 'profile_form':profile_form}, context_instance=RequestContext(request))

@login_required 
def password_change(request, send_mail=True):
	if request.method == "POST":
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			form.save()
			password = 'votre nouveau mot de passe : %s' % request.POST['new_password1']
			if send_mail==True:
				xemple_send_mail('new_user', Context({'user':request.user, 'password':password}))
			return HttpResponseRedirect(reverse('password_change_done'))
	else:
		form = PasswordChangeForm(request.user)
	return render_to_response('authentication/password_change.html', {'form': form,}, context_instance=RequestContext(request))
password_change = login_required(password_change)