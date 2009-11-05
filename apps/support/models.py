from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, UserManager
from apps.support.lists import TICKET_STATUS, TICKET_TYPE


import datetime



class TicketManager(models.Manager):
	pass

class Ticket(models.Model):
	user				=	models.ForeignKey(User, related_name='user_tickets')
	status				=	models.IntegerField(_('status'),max_length=1, default=0, choices=TICKET_STATUS)
	ticket_type			=	models.IntegerField(_('ticket Type'),max_length=1, default=0, choices=TICKET_TYPE)
	created_at			=	models.DateTimeField(_('date'))
	contact_mail		=	models.EmailField(_('contact mail'), null=True, blank=True, max_length=100)
	contact_phone		=	models.CharField(_('contact phone'), null=True, blank=True, max_length=100)
	answered			=	models.BooleanField(_('is Answered'), default=0)
	objects				=	TicketManager()
		
	class Meta:
		verbose_name = _('ticket')
		verbose_name_plural = _('tickets')
		ordering = ['-created_at']
		
	def __unicode__(self):
		return u'%s' % self.id
		
	def save(self, force_insert=False, force_update=False):
		self.created_at = datetime.datetime.now()
		super(Ticket, self).save()
		
	def is_answered(self):
		self.answered=True
		self.save()
		return True
		
	def has_new_message(self):
		self.answered=False
		self.save()
		return True
		


class Message(models.Model):
	user				=	models.ForeignKey(User, related_name='user_messages')
	ticket				=	models.ForeignKey(Ticket, related_name='ticket_messages')
	content				=	models.TextField(max_length=1000, blank=True, null=True)
	linked_file 		=	models.FileField(upload_to='support/user/%s/' % datetime.date.today(), null=True, blank=True) 
	created_at 			=	models.DateTimeField(default=datetime.datetime.now())

	class Meta:
		verbose_name = _('message')
		verbose_name_plural = _('messages')
		ordering = ['-created_at']
		
	def __unicode__(self):
		return 'Ticket %s le %s' % (self.ticket.id, self.created_at)
		
	def save(self, force_insert=False, force_update=False):
		if self.user.has_perm('is_staff'):
			self.ticket.is_answered()
		else:
			self.ticket.has_new_message()
		self.created_at = datetime.datetime.now()
		super(Message, self).save()
