from django.contrib import admin
from django.contrib.auth.models import User
from apps.emailing.models import XmailTemplate



class XmailTemplateAdmin(admin.ModelAdmin):
	list_display = ('id', 'mail_type',)
	list_display_links = ('id', 'mail_type')
admin.site.register(XmailTemplate, XmailTemplateAdmin)