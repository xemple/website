from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from apps.service.models import Service
import datetime


class Offer(models.Model):
	name			=	models.CharField(max_length=50)
	description		=	models.TextField(max_length=500)
	price			=	models.FloatField()
	cpu				=	models.FloatField()
	ram				=	models.FloatField()
	disk_space		=	models.FloatField()
	is_active		=	models.BooleanField(default=True)
	is_public		=	models.BooleanField(default=False)
	
	class Meta:
		verbose_name = _('offer')
		verbose_name_plural = _('offers')
		
	def __unicode__(self):
		return str(self.name)
	
class Subscription(models.Model):
	offer			=	models.ForeignKey(Offer)
	service			=	models.ForeignKey(Service, blank=True, null=True)
	expiracy		=	models.DateTimeField()
	user			=	models.ForeignKey(User, related_name="user_subscription")
	
	class Meta:
		verbose_name = _('subscription')
		verbose_name_plural = _('subcriptions ')
		
	def __unicode__(self):
		return str("%s / %s") % (self.user, self.offer)
	
	
class Invoice(models.Model):
	invoice_num		=	models.IntegerField()
	user			=	models.ForeignKey(User)
	first_name		=	models.CharField(max_length=30)
	last_name		=	models.CharField(max_length=30)
	address			=	models.CharField(max_length=50)
	adress_ext		=	models.CharField(max_length=50)
	city			=	models.CharField(max_length=30)
	zip_code		=	models.CharField(max_length=15)
	country			=	models.CharField(max_length=2)
	email 			= 	models.EmailField(max_length=50)
	phone			=	models.CharField(max_length=20)
	fax				=	models.CharField(max_length=20)
	cellphone		=	models.CharField(max_length=20)
	date 			= 	models.DateField(default=datetime.datetime.today)
	tva				=	models.FloatField()
	is_paid			=	models.BooleanField(default=False)
	
	class Meta:
		verbose_name = _('invoice')
		verbose_name_plural = _('invoices')
		
	def __unicode__(self):
		return str(self.invoice_num)
	

class InvoiceItem(models.Model):
	subscription	=	models.ForeignKey(Subscription)
	invoice			=	models.ForeignKey(Invoice)
	description		=	models.CharField(max_length=500)
	price			=	models.FloatField()
	quantity		=	models.IntegerField()
	
	class Meta:
		verbose_name = _('invoice item')
		verbose_name_plural = _('invoice items')
		
	def __unicode__(self):
		return str(self.invoice)
	

class Transaction(models.Model):
	invoice			=	models.ForeignKey(Invoice)
	price			=	models.FloatField()
	date 			= 	models.DateField(default=datetime.datetime.today)
	info			=	models.CharField(max_length=150)
	
	class Meta:
		verbose_name = _('transaction')
		verbose_name_plural = _('transactions')
		
	def __unicode__(self):
		return str(self.invoice)
		
		
class MiniCart(object):
	def __init__(self, item_id, quantity):
		self.item_id = item_id
		self.quantity = quantity