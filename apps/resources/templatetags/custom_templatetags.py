from django import template
from apps.support.models import Ticket, Message

register = template.Library()

@register.inclusion_tag('admin/support/ticket/ticket.html')
def display_messages(ticket_id):
    ticket = Ticket.objects.get(id__exact=ticket_id)
    message = Message.objects.filter(ticket=ticket)[0:5]
    return { 'message': message }