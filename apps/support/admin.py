from django.contrib import admin
from apps.support.models import Ticket, Message

class TicketAdmin(admin.ModelAdmin):
	pass
admin.site.register(Ticket, TicketAdmin)

class MessageAdmin(admin.ModelAdmin):
	pass
admin.site.register(Message, MessageAdmin)