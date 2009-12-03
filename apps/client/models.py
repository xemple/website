from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, UserManager
from apps.resources.countries import COUNTRY_CHOICES
from apps.resources.tools import xemple_username_generator

import datetime




class ClientProfileManager(models.Manager):
	def create_client(self, email, first_name, last_name, company, address, address_ext, zip_code, city, country, phone, fax, cellphone):
		"Creates and saves a Client with the given username, e-mail and password and base informations."
		now = datetime.datetime.now()
		username = xemple_username_generator(fn=first_name,ln=last_name)
		rand_password = User.objects.make_random_password()
		new_user = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email.strip().lower(), password="changeme")
		new_user.set_password(rand_password)
		new_user.save()
		new_profile = self.model(None, new_user.id, company, address, address_ext, zip_code, city, country, phone, fax, cellphone)
		new_profile.save()
		return new_user.username, rand_password




class ClientProfile(models.Model):
	user						=	models.ForeignKey(User, unique=True)
	company						=	models.CharField(_('company'),max_length=100, null=True, blank=True)
	address						=	models.CharField(_('address'),max_length=100)
	address_ext					=	models.CharField(_('address'),max_length=100, null=True, blank=True)
	zip_code					=	models.CharField(_('zip code'),max_length=100)
	city						=	models.CharField(_('city'),max_length=100)
	country						=	models.CharField(_('country'),max_length=2, choices=COUNTRY_CHOICES)
	phone						=	models.CharField(_('phone'),max_length=50)
	fax							=	models.CharField(_('fax'),max_length=50, null=True, blank=True)
	cellphone					=	models.CharField(_('cellphone'),max_length=50, null=True, blank=True)
	mail_expiracy_alerts 		=	models.BooleanField(_('receive expiracy alerts'), default=True)
	expiracy_countdown			=	models.IntegerField(_('expiracy mail start'), max_length=3, default=15, null=True, blank=True)
	mail_newsletter				=	models.BooleanField(_('receive newletter'), default=False)
	mail_ticket_answer 			=	models.BooleanField(_('mail ticket answer'), default=True)
	pouete 						=	models.TextField(_('note'),max_length=2000, null=True, blank=True)
	objects				=	ClientProfileManager()
		
	class Meta:
		verbose_name = _('client profile')
		verbose_name_plural = _('clients profile')
		
	def __unicode__(self):
		return self.user.username
		

"""
mail_expiracy_alerts 		=	models.BooleanField(_('receive expiracy alerts'), default=True)
expiracy_countdown			=	models.IntegerField(_('expiracy mail start'), max_length=2)
mail_newsletter				=	models.BooleanField(_('receive newletter'), default=False)
mail_ticket_answer 			=	models.BooleanField(_('mail ticket answer'), default=True)
"""