import datetime
from django.db import models
from dateutil.relativedelta import *
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext_lazy as _

from apps.service.models import Service
from apps.resources.tools import calculate_billing, calculate_vat, invoice_number_generator







class MiniCart(object):
	def __init__(self, item_id, quantity, renew_sub = None):
		self.item_id = item_id
		self.quantity = quantity
		self.renew_sub = renew_sub


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
	
	
	
	
	
class SubscriptionManager(models.Manager):
	def create_new_subscription(self, offer, user):
		new_sub = self.model(None, int(offer), None, datetime.datetime.now(), datetime.datetime.now(), user)
		new_sub.save()
		return new_sub	
	
class Subscription(models.Model):
	offer			=	models.ForeignKey(Offer)
	service			=	models.ForeignKey(Service, blank=True, null=True)
	root_expiracy	=	models.DateTimeField()
	expiracy		=	models.DateTimeField()
	user			=	models.ForeignKey(User, related_name="user_subscription")
	objects			=	SubscriptionManager()
	
	class Meta:
		verbose_name = _('subscription')
		verbose_name_plural = _('subcriptions ')
		
	def __unicode__(self):
		return str("%s / %s") % (self.user, self.offer)
		
	def has_service(self):
		answer = None
		if self.service is not None:
			answer = True
		return answer
			
	def expiracy_countdown(self):
		expiracy_delta = relativedelta(self.expiracy, datetime.date.today())
		print expiracy_delta
		return expiracy_delta
		
	def send_expiracy_alert(self):
		expiracy_delta = self.expiracy_countdown
		alarm = [relativedelta(days=+15), relativedelta(days=+10), relativedelta(days=+5)]
		answer = False
		for t in alarm:
			try :
				if expiracy_delta == t:
					send_mail('Un de vos services va expirer', 'Le Service Prout va expirer', 'from@example.com',['to@example.com'], fail_silently=False)
					answer = True
			except ValueError:
				continue
		return answer
		
	def time_is_running_out(self):
		answer = None
		alarm_delta = relativedelta(days=+15)
		result = datetime.datetime.now()+alarm_delta
		if result >= self.expiracy :
			answer = self.expiracy_countdown()
		print answer
		return answer
	
	def has_problem(self):
		answer = None
		if self.service == None:
			answer = "Server doesn't exists."
		else:
			if self.service.is_active == False:
				answer = 'Server is shuted-down.'
		if datetime.datetime.today() > self.expiracy:
			answer = 'Your subscription has expire.'
		return answer
	
	def service_name(self):
		if self.service is not None:
			answer = self.service.name
		else:
			answer = self.offer.name
		return u'%s' % answer
		
	def renew_subscription(self):
		#LOL REQUEST = ]]]]]    request.session['mycart'] = MiniCart(item_id=int(self.offer.id), quantity=int(0), renew_sub=int(self.id))
		return HttpResponseRedirect(reverse(renew_duration_choice))
	





class InvoiceManager(models.Manager):
	def generate_invoice(self, user, vat_rate):
		new_invoice = self.model(None,invoice_number_generator(), int(user.id), user.first_name, user.last_name, \
								user.get_profile().address, user.get_profile().address_ext, user.get_profile().city, \
								user.get_profile().zip_code, user.get_profile().country, user.email, user.get_profile().phone, \
								user.get_profile().fax, user.get_profile().cellphone, datetime.datetime.today(), vat_rate )
		new_invoice.save()
		return new_invoice
		
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
	date 			= 	models.DateField(default=datetime.datetime.today())
	tva				=	models.FloatField()
	is_paid			=	models.BooleanField(default=False)
	objects			=	InvoiceManager()
	
	class Meta:
		verbose_name = _('invoice')
		verbose_name_plural = _('invoices')
		ordering = ['-date']
		
	def __unicode__(self):
		return str(self.id)
	
	def get_last_item(self):
		item = self.invoice_item.latest('id')
		return item
		
	def get_last_transaction(self):
		trans = self.linked_transaction.latest('id')
		return trans
		
	def get_total_without_vat(self):
		items = self.invoice_item.all()
		total = 0
		for i in items:
			total = total+(i.total())
		return float(total)

	def get_vat_amount(self):
		total = self.get_total_without_vat()
		vat_rate, vat = calculate_vat(total)
		return round(float(vat), 2)
		
	def get_total_with_vat(self):
		total_wo_vat = self.get_total_without_vat()
		vat = self.get_vat_amount()
		total = (float(total_wo_vat)+float(vat))
		return float(total)
		
	def activate_subscriptions(self):
		subscriptions = self.invoice_item.all()
		for s in subscriptions :
			renew_time = s.quantity
			s.subscription.expiracy = datetime.date.today()+relativedelta(months=+renew_time)
			s.subscription.save()
		return True
	
	
	
	
class InvoiceItemManager(models.Manager):
	def create_invoice_item(self, subscription, invoice, item_id, quantity):
		offer = Offer.objects.get(id=item_id)
		new_invoice_item = self.model(None, subscription, invoice, offer.description, offer.price, quantity)
		new_invoice_item.save()
		return new_invoice_item
		
		
class InvoiceItem(models.Model):
	subscription	=	models.ForeignKey(Subscription)
	invoice			=	models.ForeignKey(Invoice, related_name='invoice_item')
	description		=	models.CharField(max_length=500)
	price			=	models.FloatField()
	quantity		=	models.IntegerField()
	objects			=	InvoiceItemManager()
	
	class Meta:
		verbose_name = _('invoice item')
		verbose_name_plural = _('invoice items')
		
	def __unicode__(self):
		return str(self.invoice)
		
	def get_invoice(self):
		return self.invoice.all()
		
	def total(self):
		return round(float(self.price)*int(self.quantity), 2)
	
	
	
	
	
	
class TransactionManager(models.Manager):
	def new_transaction(self, invoice, price):
		new_trans = self.model(None, invoice, price, datetime.datetime.now(), 'no informations')
		new_trans.save()
		return new_trans 
		
		
class Transaction(models.Model):
	invoice			=	models.ForeignKey(Invoice, related_name='linked_transaction')
	price			=	models.FloatField()
	date 			= 	models.DateField(default=datetime.datetime.today)
	info			=	models.CharField(max_length=150)
	frozen			=	models.BooleanField(default=True)
	objects			=	TransactionManager()
	
	class Meta:
		verbose_name = _('transaction')
		verbose_name_plural = _('transactions')
		
	def __unicode__(self):
		return str(self.id)
		
	def validate(self):
		self.invoice.is_paid = True
		self.invoice.save()
		self.frozen = False
		self.date = datetime.date.today()
		self.invoice.activate_subscriptions()
		self.save()
		return True
		
	def cancel(self):
		self.frozen = False
		self.date = datetime.date.today()
		self.save()
		return True
		
		
		
__all__ = ['MyCart']

class CartItem(object):
	def __init__(self, item_id, name, quantity, price, renew_sub = None):
		self.item_id = item_id
		self.name = name
		self.quantity = quantity
		self.price = price
		self.renew_sub = renew_sub



class MyCart(object):
	def __init__(self):
		self._items = SortedDict()

	def get_item(self, item_id):
		return self._items.get(item_id, None)

	def add_item(self, item_id, renew=False):
		print "OMG"
		if renew == False :
			item = Offer.objects.get(id__exact=item_id)
			price = item.price
			name = item.name
		else:
			item = Subscription.objects.get(id__exact=item_id)
			price = item.offer.price
			name = item.offer.name
		print "zzzzz"
		test = self.get_item(item_id)
		print "xxxxx"
		print test
		if test is None:
			print "LOOOLLLLLL"
			item = CartItem(
				item_id = str(item.id),
				name = str(name),
				quantity = int(1),
				price = float(price),
			)
		self._items[item_id] = item
		return item

	def update_item(self, item_id, count):
		item = self.get_item(item_id)
		if item is not None:
			item.set_count(count)
			if count <= 0:
				del self._items[item_id]
			else:
				self._items[item_id] = item
		elif count > 0:
			item = self.add_item(item_id)
			if count > 1:
				item.inc_count(count-1)
			self._items[item_id] = item
		return item

	def remove_item(self, item_id):
		item = self.get_item(item_id)
		if item is not None:
			item.inc_count(-1)
			if item.units <= 0:
				del self._items[item_id]
			else:
				self._items[item_id] = item
		return item


	def items(self):
		return self._items.values()

	def empty(self):
		self._items = {}