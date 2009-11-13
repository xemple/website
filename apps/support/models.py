from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, UserManager
from apps.support.lists import TICKET_STATUS, TICKET_TYPE, KNOW_TYPE



import datetime



class TicketManager(models.Manager):
	pass

class Ticket(models.Model):
	user				=	models.ForeignKey(User, related_name='user_tickets')
	status				=	models.IntegerField(_('status'),max_length=1, default=0, choices=TICKET_STATUS)
	ticket_type			=	models.IntegerField(_('ticket Type'),max_length=1, default=0, choices=TICKET_TYPE)
	created_at			=	models.DateTimeField(_('date'), default = datetime.datetime.now())
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
		# tempo because on va need LOL =]]]]
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
	#subscription		=	models.ForeignKey(Subscription, related_name='related_tickets')
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
		# L'utilisateur peut choisir de simplement uploader un ficher en reponse a une demande d'admin
		if self.content == '' and self.linked_file == None:
			pass
		else:
			super(Message, self).save()
		

class Knowledge(models.Model):
	user				=	models.ForeignKey(User, related_name='knowledge_contribution')
	title				=	models.CharField(max_length=150)
	content				=	models.TextField(max_length=5000)
	knowledge_type		=	models.CharField(max_length=20,default='misc', choices=KNOW_TYPE)
	created_at			=	models.DateTimeField(default = datetime.datetime.now())
	edited_at			=	models.DateTimeField(default = datetime.datetime.now())
	is_active			=	models.BooleanField(default=False)
	
	class Meta:
		verbose_name = _('Knowledge')
		verbose_name_plural = _('Knowledges')
		ordering = ['-created_at']
		
	def __unicode__(self):
		return u'%s' % self.title
		
	def save(self, force_insert=False, force_update=False):
		if self.user.has_perm('is_staff'):
			self.is_active = True
		self.edited_at = datetime.datetime.now()
		super(Knowledge, self).save()