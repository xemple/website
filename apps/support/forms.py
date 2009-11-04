from django.forms import ModelForm
from apps.support.models import Message, Ticket


class MessageForm(ModelForm):
	class Meta:
		model = Message
		fields = ('content', 'linked_file')
		
		
class TicketForm(ModelForm):
	class Meta:
		model = Ticket
		fields = ('type', 'contact_mail', 'contact_phone')
