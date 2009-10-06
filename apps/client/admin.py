from django.contrib import admin
from apps.client.models import Client, Contact

class ClientAdmin(admin.ModelAdmin):
	list_display = ('username', 'first_name', 'last_name', 'company', 'email', 'date_joined', 'last_login', 'is_active')
	list_filter = ('is_active', 'date_joined')
	search_fields = ['username', 'last_name', 'company']
	fieldsets = (
	        (None, {
	            'fields': ('username', 'first_name', 'last_name', 'email', 'company', 'address', 'zip_code', 'city', 'country', 'date_joined', 'last_login', 'is_active')
	        }),
	        ('Advanced options', {
	            'classes': ('collapse',),
	            'fields': ('password', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
	        }),
	    )

class ContactAdmin(admin.ModelAdmin):
	list_display = ('client', 'contact_type', 'first_name', 'last_name', 'email', 'phone', 'fax', 'cellphone')

admin.site.register(Client, ClientAdmin)
admin.site.register(Contact, ContactAdmin)