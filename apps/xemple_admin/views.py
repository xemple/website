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




@permission_required('is_staff')
def index(request):
	return render_to_response('xemple_admin/index.html', {}, context_instance=RequestContext(request))
	
@permission_required('is_staff')
def staff_index(request):
	return render_to_response('xemple_admin/staff.html', {}, context_instance=RequestContext(request))