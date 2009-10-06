# -*- coding: utf-8 -*-
import datetime
from django.conf import settings
from django.db import models, transaction
from django.contrib.auth.models import User
from apps.client.models import Client, Contact
from apps.service.models import Service



class Mailbox(models.Model):
	domain			=	models.ForeignKey(Service, related_name='mail_domain')
	active			=	models.BooleanField(default=True)
	username		=	models.CharField(max_length=25)
	password		=	models.CharField(max_length=50)
	created_at		=	models.DateTimeField()
	edited_at		=	models.DateTimeField()
	
	class Meta:
		verbose_name = 'mailbox'
		verbose_name_plural = 'mailboxes'
		
	def __unicode__(self):
		return self.username
		
	def save(self, force_insert=False, force_update=False):
		self.edited_at = datetime.datetime.now()
		super(Mailbox, self).save()
	
	
class Repondeur(models.Model):
	mailbox			=	models.ForeignKey(Mailbox, related_name='repondeur')
	active			=	models.BooleanField(default=True)
	message			=	models.TextField(max_length=2000)
	created_at		=	models.DateTimeField()
	edited_at		=	models.DateTimeField()
	
	class Meta:
		verbose_name = 'repondeur'
		verbose_name_plural = 'repondeurs'
		
	def __unicode__(self):
		return self.path
		
	def save(self, force_insert=False, force_update=False):
		self.edited_at = datetime.datetime.now()
		super(Repondeur, self).save()
	

class Alias(models.Model):
	domain			=	models.ForeignKey(Service, related_name='mail_alias')
	active			=	models.BooleanField(default=True)
	address			=	models.CharField(max_length=200)
	goto			=	models.CharField(max_length=200)
	created_at		=	models.DateTimeField()
	edited_at		=	models.DateTimeField()
	
	class Meta:
		verbose_name = 'Alias'
		verbose_name_plural = 'Alias'
		
	def __unicode__(self):
		return self.address
		
	def save(self, force_insert=False, force_update=False):
		self.edited_at = datetime.datetime.now()
		super(Alias, self).save()