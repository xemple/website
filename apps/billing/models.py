# -*- coding: utf-8 -*-
import datetime
from django.conf import settings
from django.db import models, transaction
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from apps.client.models import Client, Contact
from apps.service.models import Service

		
		
class Offer(models.Model):
	name			=	models.CharField(max_length=100)
	description		=	models.TextField(max_length=500)
	price			=	models.FloatField()
	period			=	models.IntegerField()
	offer			=	models.ForeignKey('self', related_name='dependences', null=True, blank=True)
	is_hosting		=	models.BooleanField(default=0)
	is_domain		=	models.BooleanField(default=0)
	domain_ext		=	models.CharField(max_length=10, unique=True, null=True, blank=True)
	
	class Meta:
		verbose_name = 'offer'
		verbose_name_plural = 'offers'

	def __unicode__(self):
		return self.name



class SubscriptionManager(models.Manager):
	def create_subscription(self, offer, quantity, service=None):
		now = datetime.datetime.now()
		exp_date = now + datetime.timedelta(days = offer.period)
		new_subscription = self.model(None, service, exp_date, offer.id, quantity, 0, now, now)
		new_subscription.save()
		return new_subscription
	
	
class Subscription(models.Model):
	service			=	models.ForeignKey(Service, related_name='subscription', null=True)
	expire_at		=	models.DateTimeField()
	offer			=	models.ForeignKey(Offer, related_name='subscription')
	quantity		=	models.PositiveIntegerField()
	status			=	models.BooleanField()
	created_at		=	models.DateTimeField()
	edited_at		=	models.DateTimeField()	
	objects			=	SubscriptionManager()
	
	class Meta:
		verbose_name = 'subscription'
		verbose_name_plural = 'subscriptions'

	def __unicode__(self):
		return self.offer.name
		
	def smart_time_left(self):
		diff = self.expire_at - datetime.datetime.now()
		minutes, seconds = divmod(diff.seconds, 60)
		hours, minutes = divmod(minutes, 60)
		return "%d days, %d:%d:%d" % (diff.days, hours, minutes, seconds)
		
	def save(self, force_insert=False, force_update=False):
		self.edited_at = datetime.datetime.now()
		super(Subscription, self).save()


class QuoteManager(models.Manager):
	def create_new_quote(self, client):
		now = datetime.datetime.now()
		contact = Contact.objects.get(client=client.id, contact_type="client")
		new_quote = self.model(None, client.id, 999999999, client.first_name, client.last_name, client.company, client.address,\
								client.city, client.zip_code, client.country, contact.phone, contact.cellphone, contact.fax, contact.email, now, 0, None)
		new_quote.save()
		new_quote.quote_number=new_quote.id
		new_quote.save()
		return new_quote
		
		

		
class Quote(models.Model):
	client			=	models.ForeignKey(User, related_name='quote')
	quote_number	=	models.PositiveIntegerField(unique=True)
	first_name		=	models.CharField(max_length=30)
	last_name		=	models.CharField(max_length=30)
	company			=	models.CharField(max_length=30, null=True, blank=True)
	address			=	models.CharField(max_length=100)
	city			=	models.CharField(max_length=30)
	zip_code		=	models.CharField(max_length=20)
	country			=	models.CharField(max_length=100)
	phone			=	models.CharField(max_length=40)
	cellphone		=	models.CharField(max_length=40, null=True, blank=True)
	fax				=	models.CharField(max_length=40, null=True, blank=True)
	email			=	models.EmailField()
	quote_date		=	models.DateTimeField()
	is_bill			=	models.BooleanField()
	bill_date		=	models.DateField(null=True, blank=True)
	objects			=	QuoteManager()
	
	class Meta:
		verbose_name = 'quote'
		verbose_name_plural = 'quotes'

	def __unicode__(self):
		return self.user

	def is_now_a_bill(self, force_insert=False, force_update=False):
		self.is_bill = True
		self.bill_date = datetime.datetime.now()
		super(Quote, self).save()



	

class QuoteItem(models.Model):
	quote			=	models.ForeignKey(Quote, related_name='quote_item')
	description		=	models.CharField(max_length=100)
	price			=	models.FloatField()
	quantity		=	models.PositiveIntegerField()
	subscription	=	models.ForeignKey(Subscription, null=True, blank=True)
	
	class Meta:
		verbose_name = 'quote item'
		verbose_name_plural = 'quote items'

	def __unicode__(self):
		return self.quote



	
