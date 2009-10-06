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
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from apps.service.models import SiteTechnology, Site
from apps.logging.models import Log

def test(request):
	lol = SiteTechnology.objects.check_last_revision('php')
	prout =  Site.objects.get(id=1)
	prout.upgrade_technology()
	user = User.objects.get(id=2)
	Log.objects.log_event(user, 'fait caca', prout, request.META['REMOTE_ADDR'])
	return render_to_response('test/test.html', {'lol':lol}, context_instance=RequestContext(request))