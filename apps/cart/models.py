# -*- coding: utf-8 -*-
from django.utils.datastructures import SortedDict
from apps.billing.models import Offer

__all__ = ['Cart']

class CartItem(object):
	def __init__(self, sku, title, description, price, count=0):
		self.sku = sku
		self.title = title
		self.description = description
		self.price = price
		self.units = count
		self.total = 0

	def inc_count(self, inc):
		self.units = self.units + inc;
		self.total = self.units * self.price
		
	def set_count(self, count):
		self.units = count
		self.total = self.units * self.price


class Cart(object):
	def __init__(self):
		self._items = SortedDict()
		
	def get_item(self, sku):
		return self._items.get(sku, None)

	def get_total_price(self):
		total = 0
		for item in self._items.values():
			total += item.total
		return total

	def get_total_count(self):
		total = 0
		for item in self._items.values():
			total += item.count
		return total

	def add_item(self, sku):
		# get product associated to sku
		item = Offer.objects.get(id__exact=sku)
		product = item
		item = self.get_item(sku)
		if item is None:
			item = CartItem(
				sku = sku,
				title = product.name,
				description = product.description,
				price = product.price,
			)
		item.inc_count(+1)
		self._items[sku] = item
		return item

	def update_item(self, sku, count):
		item = self.get_item(sku)
		if item is not None:
			item.set_count(count)
			if count <= 0:
				del self._items[sku]
			else:
				self._items[sku] = item
		elif count > 0:
			item = self.add_item(sku)
			if count > 1:
				item.inc_count(count-1)
			self._items[sku] = item
		return item
		
	def remove_item(self, sku):
		item = self.get_item(sku)
		if item is not None:
			item.inc_count(-1)
			if item.units <= 0:
				del self._items[sku]
			else:
				self._items[sku] = item
		return item
		
	def inc_item_count(self, sku, count):
		item = self.get_item(sku)
		if item is not None:
			item.inc_count(count)
			if item.units <= 0:
				del self._items[sku]
			else:
				self._items[sku] = item
		elif count > 0:
			item = self.add_item(sku)
			if count > 1:
				item.inc_count(count-1)
			self._items[sku] = item
		return item
			
	def has_items(self):
		return len(self._items) != 0

	def items(self):
		return self._items.values()

	def empty(self):
		self._items = {}