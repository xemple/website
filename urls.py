# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import databrowse
from django.contrib.auth.decorators import login_required
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns('',
	(r'^', include('apps.front.urls')),
	(r'^manager/', include('apps.manager.urls')),
	# temporary
	#(r'^offers/', include('apps.billing.urls')),
	#(r'^offer/', include('apps.billing.urls')),
	# /temporary
	#(r'^billing/', include('apps.billing.urls')),
	(r'^admin/(.*)', admin.site.root),
	(r'^xadmin/', include('apps.xemple_admin.urls')),
	
)


if settings.DEBUG == True :
	urlpatterns += patterns('',(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.PROJECT_PATH+'/media/', 'show_indexes': True}),)

