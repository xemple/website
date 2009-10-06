# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, UserManager
from apps.ressources.country import COUNTRY_CHOICES

import settings, datetime
			

def generate_username(fn, ln):
	fn, ln =fn.strip(), ln.strip()
	first_letters = '%s%s' % (fn[:1], ln[:1])
	p1 = first_letters.upper()
	total_user = Client.objects.count()
	user_number = total_user+1
	username = '%s-%s@xemple' % (p1, user_number)
	return '%s' % username


class ClientManager(UserManager):
	def create_client(self, email, first_name, last_name, company, address, zip_code, city, country):
		"Creates and saves a Client with the given username, e-mail and password and base informations."
		now = datetime.datetime.now()
		user = self.model(None, 'placeholder', first_name, last_name, email.strip().lower(), 'placeholder', False, True, False, now, now, None, company, address, zip_code, city, country)
		user.username = generate_username(fn=first_name,ln=last_name)
		password = UserManager.make_random_password
		if password:
			user.set_password(password)
		else:
			user.set_unusable_password()
		user.save()
		return user,user.username,password

class Client(User):
	company				=	models.CharField(_('company'),max_length=100, null=True, blank=True)
	address				=	models.CharField(_('address'),max_length=100)
	zip_code			=	models.CharField(_('zip code'),max_length=100)
	city				=	models.CharField(_('city'),max_length=100)
	country				=	models.CharField(_('country'),max_length=2, choices=COUNTRY_CHOICES)
	objects				=	ClientManager()

	
		




CONTACT_TYPE = (
				('tech','Technical'),
				('billing','Billing'),
				('client','Client'),
				)
				
class ContactManager(models.Manager):
	def create_client_contact(self, client, phone, fax, cellphone):
		client_contact	=	self.model(None, client.id, 'client', client.first_name, client.last_name, client.email, phone, fax, cellphone)
		client_contact.save()
		return client_contact
		
class Contact(models.Model):
	client				=	models.ForeignKey(Client, related_name = 'contact')
	contact_type		=	models.CharField(_('contact type'),max_length=100, choices=CONTACT_TYPE)
	first_name			=	models.CharField(_('first name'),max_length=100)
	last_name			=	models.CharField(_('last name'),max_length=100)
	email				=	models.EmailField(_('e-mail address'),max_length=100)		
	phone				=	models.CharField(_('phone'),max_length=50)
	fax					=	models.CharField(_('fax'),max_length=50, null=True, blank=True)
	cellphone			=	models.CharField(_('cellphone'),max_length=50, null=True, blank=True)
	objects				=	ContactManager()
	
	
	class Meta:
		verbose_name = _('contact')
		verbose_name_plural = _('contacts')
		ordering = ('client', 'contact_type')
		
	def __unicode__(self):
		return self.contact_type