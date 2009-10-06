# -*- coding: utf-8 -*-
import datetime
from django.conf import settings
from django.db import models, transaction
from django.contrib.auth.models import User, UserManager
from apps.service.models import Service, Site
from apps.ressources.crypto import get_hexdigest, check_password, make_random_password

UNUSABLE_PASSWORD = '!'



#######################
#######################
#######################
'definir une politique de format des logins db'
#######################
#######################
#######################




class DatabaseServerManager(models.Manager):
	def create_new_databaseserver(self, service, password=None):
		#########################################################
		# ASPIK_TAG --- aspik.create_new_dbserver() 			#
		#########################################################
		now = datetime.datetime.now()
		tempo_login = make_random_password
		new_dbs = self.model(None, service, tempo_login, 'placeholder', now, now)
		new_dbs.save()
		login = '%s%s' % ('new_server', new_dbs.admin_login)
		if password:
			new_dbs.set_password(password)
		else:
			raw_password = make_random_password
			new_dbs.set_password(raw_password)
		new_dbs.save()
		return new_dbs


class DatabaseServer(models.Model):
	service			=	models.ForeignKey(Service, related_name='service_dbserver')
	admin_login		=	models.CharField(max_length=25)
	admin_password	=	models.CharField(max_length=50)
	created_at		=	models.DateTimeField()
	edited_at		=	models.DateTimeField()
	
	class Meta:
		verbose_name = 'database server'
		verbose_name_plural = 'database servers'
		
	def __unicode__(self):
		return self.service.name
		
	def save(self, force_insert=False, force_update=False):
		self.edited_at = datetime.datetime.now()
		super(DatabaseServer, self).save()
		
	def set_password(self, raw_password):
		import random
		algo = 'sha1'
		salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
		hsh = get_hexdigest(algo, salt, raw_password)
		self.admin_password = '%s$%s$%s' % (algo, salt, hsh)

	def check_password(self, raw_password):
		if '$' not in self.admin_password:
			is_correct = (self.admin_password == get_hexdigest('md5', '', raw_password))
			if is_correct:
				self.set_password(raw_password)
				self.save()
			return is_correct
		return check_password(raw_password, self.admin_password)

	def set_unusable_password(self):
		self.admin_password = UNUSABLE_PASSWORD

	def has_usable_password(self):
		return self.admin_password != UNUSABLE_PASSWORD




class Database(models.Model):
	site			=	models.ForeignKey(Site, related_name='site_db')
	db_server		=	models.ForeignKey(DatabaseServer, related_name='db_server')
	type			=	models.CharField(max_length=10)
	name			=	models.CharField(max_length=100)
	created_at		=	models.DateTimeField()
	edited_at		=	models.DateTimeField()
	
	def __unicode__(self):
		return self.name
		
	def save(self, force_insert=False, force_update=False):
		self.edited_at = datetime.datetime.now()
		super(Database, self).save()
	
	
	
class DatabaseUserManager(models.Manager):
	def create_new_databaseuser(self, client, database, password=None):
		#########################################################
		# ASPIK_TAG --- aspik.create_new_dbuser(self, version) 	#
		#########################################################
		now = datetime.datetime.now()
		tempo_login = make_random_password
		new_dbu = self.model(None, database, tempo_login, 'placeholder', now, now)
		new_dbu.save()
		login = '%s%s' % ('nouveau_user', new_dbu.login)
		if password:
			new_dbu.set_password(password)
		else:
			raw_password = make_random_password
			new_dbu.set_password(raw_password)
		new_dbu.save()
		return new_dbu
		
	
class DatabaseUser(models.Model):
	database		=	models.ForeignKey(Database, related_name='db_user')
	login			=	models.CharField(max_length=25, unique=True)
	password		=	models.CharField(max_length=50)
	created_at		=	models.DateTimeField()
	edited_at		=	models.DateTimeField()
	objects			=	DatabaseUserManager()
	
	
	class Meta:
		verbose_name = 'database user'
		verbose_name_plural = 'database users'
		
	def __unicode__(self):
		return self.login
		
	def save(self, force_insert=False, force_update=False):
		self.edited_at = datetime.datetime.now()
		super(DatabaseUser, self).save()
		
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