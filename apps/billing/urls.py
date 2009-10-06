# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('apps.billing.views',
    
	url(r'^select_offer/$','select_offer', name='select_offer'),
	url(r'^select_options/(?P<offer_id>\d+)/$','select_options', name='select_options'),
	url(r'^domain_choice/$', 'domain_choice', name='domain_choice'),
	url(r'^dn_check_domain=(?P<check_domain>.*?)/$', 'dn_check_domain', name='dn_check_domain'),

)