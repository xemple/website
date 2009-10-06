# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('apps.client.views',
    
	url(r'^new/$','client_new', name='client_new'),

)