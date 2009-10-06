from django.contrib import admin
from apps.domain.models import DnsZone, DnsDomain


class DnsZoneAdmin(admin.ModelAdmin):
	pass


class DnsDomainAdmin(admin.ModelAdmin):
	pass
	
	
admin.site.register(DomainZone, DnsZoneAdmin)
admin.site.register(DnsDomain, DnsDomainAdmin)

