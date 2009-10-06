# -*- coding: utf-8 -*-
import datetime
from django.conf import settings
from django.db import models, transaction
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from apps.client.models import Client



class VZTemplate(models.Model):
	filename		=	models.FilePathField(max_length=200)
	name			=	models.CharField(max_length=200)
	version			=	models.CharField(max_length=200)
	is_active		=	models.BooleanField(default=True)
	created_at		=	models.DateTimeField(default=datetime.datetime.now)
	edited_at		=	models.DateTimeField(default=datetime.datetime.now)
	
	def __unicode__(self):
		return self.name
	
	def save(self, force_insert=False, force_update=False):
		self.edited_at = datetime.datetime.now()
		super(VZTemplate, self).save()



class SiteTechnologyManager(models.Manager):
		def getlastrev_sort(x,y):
			import re
			def getNum(str): return float(re.findall(r'\d+',str)[0])
			return cmp(getNum(x),getNum(y))
		
		def check_last_revision(self, type):
			li = self.filter(type=type, beta=False)
			for a in li[:1]:
				li = a.revision
			return li



class SiteTechnology(models.Model):
	is_specific		=	models.BooleanField(default=True)
	type			=	models.CharField(max_length=4)
	revision		=	models.CharField(max_length=5)
	beta			=	models.BooleanField(default=False)
	autoupdate		=	models.BooleanField(default=True)
	created_at		=	models.DateTimeField(default=datetime.datetime.now)
	edited_at		=	models.DateTimeField(default=datetime.datetime.now)
	objects			=	SiteTechnologyManager()
	
	class Meta:
		verbose_name = 'site technology'
		verbose_name_plural = 'site technologies'
		ordering = ['-revision']
		
	def __unicode__(self):
		return '%s %s' % (self.type, self.revision)
		
	def save(self, force_insert=False, force_update=False):
		self.edited_at = datetime.datetime.now()
		super(SiteTechnology, self).save()
	
	def check_for_upgrade(self):
		latest = SiteTechnology.objects.check_last_revision(self.type)
		if str(latest) > str(self.revision):
			return 'An upgrade is avaiable from %s to %s' % (self.revision, latest), True, latest
		else:
			return 'You are up to date', False, latest



class ServiceManager(models.Manager):
	def create_new_service(self, client, name):
		now = datetime.datetime.now()
		new_service = self.model(None, client.id, name, now, now)
		new_service.save()
		return new_service



class Service(models.Model):
	client			=	models.ForeignKey(Client, related_name='service')
	name			=	models.CharField(max_length=100)
	created_at		=	models.DateTimeField(default=datetime.datetime.now)
	edited_at		=	models.DateTimeField(default=datetime.datetime.now)
	objects			=	ServiceManager()

	class Meta:
		verbose_name = 'service'
		verbose_name_plural = 'services'

	def __unicode__(self):
		return self.name
		
	def save(self, force_insert=False, force_update=False):
		self.edited_at = datetime.datetime.now()
		super(Service, self).save()


	
class HostingService(Service):
	ip				=	models.IPAddressField()
	root			=	models.CharField(max_length=200)
	template		=	models.CharField(max_length=200)



class DomainService(Service):
	domain			=	models.CharField(max_length=200)	



class Site(models.Model):
	domain			=	models.ForeignKey(Service, related_name='attached_site')
	technology		=	models.ForeignKey(SiteTechnology, related_name='used_on_site')
	name			=	models.CharField(max_length=200)
	created_at		=	models.DateTimeField(default=datetime.datetime.now)
	edited_at		=	models.DateTimeField(default=datetime.datetime.now)
	
	class Meta:
		verbose_name = 'site'
		verbose_name_plural = 'sites'
		
	def __unicode__(self):
		return self.name
	
	def save(self, force_insert=False, force_update=False):
		self.edited_at = datetime.datetime.now()
		super(Site, self).save()
		
	def upgrade_technology(self):
		message, upgrade, version = self.technology.check_for_upgrade()
		if upgrade == True:
			last_tech = SiteTechnology.objects.get(revision = str(version))
			#########################################################
			# ASPIK_TAG --- aspik.upgrade_technology(self, version) #
			#########################################################
			self.technology = last_tech
			self.save()
			update_message = 'Your version has been upgraded succesfully with the last version'
		else:
			update_message = 'Your version was already up to date'
		print update_message
		return True, update_message
			
