# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import databrowse
from django.contrib.auth.decorators import login_required
from django.contrib import admin

admin.autodiscover()





urlpatterns = patterns('',
	(r'^', include('apps.publicweb.urls')),
	(r'^manager/', include('apps.manager.urls')),
	(r'^client/', include('apps.client.urls')),
	(r'^billing/', include('apps.billing.urls')),
	(r'^cart/', include('apps.cart.urls')),
	(r'^admin/(.*)', admin.site.root),
)





urlpatterns += patterns('apps.testservers.test',
    
	url(r'^test/$','test', name='test'),

)









if settings.DEBUG == True :
	urlpatterns += patterns('',(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.PROJECT_PATH+'/media/', 'show_indexes': True}),)
