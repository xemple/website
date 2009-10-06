from django.contrib import admin
from apps.service.models import Service, HostingService, DomainService, Site, VZTemplate, SiteTechnology

class ServiceAdmin(admin.ModelAdmin):
	pass
	
class DomainServiceAdmin(admin.ModelAdmin):
	pass
	
class HostingServiceAdmin(admin.ModelAdmin):
	pass
	
class SiteAdmin(admin.ModelAdmin):
	pass

class VZTemplateAdmin(admin.ModelAdmin):
	pass
	
class SiteTechnologyAdmin(admin.ModelAdmin):
	list_display = ('type','revision')
	
	
admin.site.register(Service, ServiceAdmin)
admin.site.register(DomainService, DomainServiceAdmin)
admin.site.register(HostingService, HostingServiceAdmin)
admin.site.register(Site, SiteAdmin)
admin.site.register(VZTemplate, VZTemplateAdmin)
admin.site.register(SiteTechnology, SiteTechnologyAdmin)