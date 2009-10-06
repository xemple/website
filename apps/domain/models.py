# -*- coding: utf-8 -*-
import datetime
from django.conf import settings
from django.db import models, transaction
from django.contrib.auth.models import User
from apps.client.models import Client, Contact
from apps.service.models import Service




class DomainContact(models.Model):
	domain			=	models.ForeignKey(Service, related_name='domain_contact')
	type			=	models.CharField(max_length=5)
	contact			=	models.ForeignKey(Contact, related_name='domain_ext')
	created_at		=	models.DateTimeField()
	edited_at		=	models.DateTimeField()
	
	class Meta:
		verbose_name = 'domain contact'
		verbose_name_plural = 'domain contacts'
		
	def __unicode__(self):
		return self.contact
		
	def save(self, force_insert=False, force_update=False):
		self.edited_at = datetime.datetime.now()
		super(DomainContact, self).save()
	
	
	
class Dns(models.Model):
	domain			=	models.ForeignKey(Service, related_name='service_dns')
	host			=	models.CharField(max_length=100)
	type			=	models.CharField(max_length=100)
	data			=	models.CharField(max_length=100)
	created_at		=	models.DateTimeField()
	edited_at		=	models.DateTimeField()
	
	class Meta:
		verbose_name = 'dns'
		verbose_name_plural = 'dns'
		
	def __unicode__(self):
		return self.host
		
	def save(self, force_insert=False, force_update=False):
		self.edited_at = datetime.datetime.now()
		super(Dns, self).save()
	