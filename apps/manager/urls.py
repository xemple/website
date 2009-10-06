# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.utils.translation import ugettext as _



urlpatterns = patterns('apps.manager.views',

	url(r'^$', 'manager_login', name='manager_login'),
	url(r'^dashboard/', 'manager_dashboard', name='manager_dashboard'),
	url(r'^tdashboard/$', 'manager_tdashboard', name='manager_tdashboard'),
	url(r'^tadmin/$', 'manager_tadmin', name='manager_tadmin'),
	url(r'^tpanel/$', 'manager_tpanel', name='manager_tpanel'),		
)