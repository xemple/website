from django.contrib import admin
from apps.domain.models import DomainContact, Dns


class DomainContactAdmin(admin.ModelAdmin):
	pass


class DnsAdmin(admin.ModelAdmin):
	pass
	
	
admin.site.register(DomainContact, DomainContactAdmin)
admin.site.register(Dns, DnsAdmin)

