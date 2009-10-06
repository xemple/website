from django.contrib import admin
from apps.client.models import ClientProfile
from django.contrib.auth.models import User

class ClientProfileAdmin(admin.ModelAdmin):
	pass
admin.site.register(ClientProfile, ClientProfileAdmin)

