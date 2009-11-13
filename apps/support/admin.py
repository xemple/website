from django.contrib import admin
from apps.support.models import  Ticket, Message, Knowledge



class TicketAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'ticket_type', 'status', 'answered', 'created_at')
	list_display_links = ('id', 'user')
	radio_fields = {'status': admin.HORIZONTAL}
	def prout(self):
		print 'prout'
	
admin.site.register(Ticket, TicketAdmin)



class MessageAdmin(admin.ModelAdmin):
	list_display = ('ticket', 'id', 'content', 'user', 'created_at')
	list_display_links = ('id', 'content')

	
admin.site.register(Message, MessageAdmin)



class KnowledgeAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'edited_at', 'is_active')
	list_display_links = ('title',)

	
admin.site.register(Knowledge, KnowledgeAdmin)