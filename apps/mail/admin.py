from django.contrib import admin
from apps.mail.models import Mailbox, Repondeur, Alias


class MailboxAdmin(admin.ModelAdmin):
	pass


class RepondeurAdmin(admin.ModelAdmin):
	pass
	
	
class AliasAdmin(admin.ModelAdmin):
	pass

admin.site.register(Mailbox, MailboxAdmin)
admin.site.register(Repondeur, RepondeurAdmin)
admin.site.register(Alias, AliasAdmin)
