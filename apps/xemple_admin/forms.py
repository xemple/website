from django.forms import ModelForm
from apps.support.models import Message, Ticket, Knowledge


class MessageForm(ModelForm):
	class Meta:
		model = Message
		fields = ('content', 'linked_file')
		
		
class TicketForm(ModelForm):
	class Meta:
		model = Ticket
		fields = ('ticket_type', 'status')


class KnowledgeForm(ModelForm):
	class Meta:
		model = Knowledge
		fields = ('title', 'knowledge_type', 'content')