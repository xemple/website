# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.utils.translation import ugettext as _



urlpatterns = patterns('django.views.generic.simple',

	url(r'^$', 'direct_to_template', {'template': 'front/index.html'}, name='front_index'),	
	url(r'^cube/$', 'direct_to_template', {'template': 'front/cube.html'}, name='front_cube'),	
	url(r'^labs/$', 'direct_to_template', {'template': 'front/labs.html'}, name='front_labs'),
	url(r'^technology/$', 'direct_to_template', {'template': 'front/technology.html'}, name='front_technology'),		
	url(r'^status/$', 'direct_to_template', {'template': 'front/status.html'}, name='front_status'),
	url(r'^why/$', 'direct_to_template', {'template': 'front/why.html'}, name='front_why'),	
	url(r'^faq/$', 'direct_to_template', {'template': 'front/faq.html'}, name='front_faq'),
	url(r'^about/$', 'direct_to_template', {'template': 'front/about.html'}, name='front_about'),
					


)