# -*- coding: utf-8 -*-
import datetime
from django.conf import settings
from django.db import models, transaction
from django.contrib.auth.models import User
from apps.client.models import Client
from apps.service.models import Service, Site
from apps.ressources.crypto import get_hexdigest, check_password, make_random_password

UNUSABLE_PASSWORD = '!'


class FTPUserManager(models.Manager):
	def create_new_ftpuser(self, client, password):
		now = datetime.datetime.now()
		new_ftpu = self.model(None, client, True, 'A CHANGER', 'Placeholder', now, now)
		new_ftpu.save()
		if password:
			new_ftpu.set_password(password)
		else:
			raw_password = make_random_password
			new_ftpu.set_password(raw_password)
		new_ftpu.save()
		return new_ftpu

class FTPUser(models.Model):
	owner			=	models.ForeignKey(Client, related_name='ftp_access')
	active			=	models.BooleanField(default=True)
	login			=	models.CharField(max_length=25)
	password		=	models.CharField(max_length=50)
	created_at		=	models.DateTimeField(default=datetime.datetime.now)
	edited_at		=	models.DateTimeField(default=datetime.datetime.now)
	objects			=	FTPUserManager()
	
	class Meta:
		verbose_name = 'FTP user'
		verbose_name_plural = 'FTP users'
		
	def __unicode__(self):
		return self.login
		
	def save(self, force_insert=False, force_update=False):
		self.edited_at = datetime.datetime.now()
		super(FTPUser, self).save()
		
	def set_password(self, raw_password):
		import random
		algo = 'sha1'
		salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
		hsh = get_hexdigest(algo, salt, raw_password)
		self.password = '%s$%s$%s' % (algo, salt, hsh)

	def check_password(self, raw_password):
		if '$' not in self.password:
			is_correct = (self.password == get_hexdigest('md5', '', raw_password))
			if is_correct:
				self.set_password(raw_password)
				self.save()
			return is_correct
		return check_password(raw_password, self.password)

	def set_unusable_password(self):
		self.password = UNUSABLE_PASSWORD

	def has_usable_password(self):
		return self.password != UNUSABLE_PASSWORD
	

class FTPDir(models.Model):
	site			=	models.ForeignKey(Site, related_name='site_ftp_dir')
	path			=	models.CharField(max_length=150)
	ftp				=	models.ForeignKey(FTPUser, related_name='ftp_directory')
	created_at		=	models.DateTimeField(default=datetime.datetime.now)
	edited_at		=	models.DateTimeField(default=datetime.datetime.now)
	
	class Meta:
		verbose_name = 'FTP directory'
		verbose_name_plural = 'FTP directories'
		
	def __unicode__(self):
		return self.site.name
		
	def save(self, force_insert=False, force_update=False):
		self.edited_at = datetime.datetime.now()
		super(FTPDir, self).save()