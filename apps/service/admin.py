from django.contrib import admin
from django.contrib.auth.models import User
from apps.service.models import Node, Service



class NodeAdmin(admin.ModelAdmin):
	pass
admin.site.register(Node, NodeAdmin)


class ServiceAdmin(admin.ModelAdmin):
	pass
admin.site.register(Service, ServiceAdmin)