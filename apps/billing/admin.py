from django.contrib import admin
from django.contrib.auth.models import User
from apps.billing.models import Offer, Subscription, Invoice, InvoiceItem, Transaction



class OfferAdmin(admin.ModelAdmin):
	pass
admin.site.register(Offer, OfferAdmin)


class SubscriptionAdmin(admin.ModelAdmin):
	pass
admin.site.register(Subscription, SubscriptionAdmin)


class InvoiceAdmin(admin.ModelAdmin):
	pass
admin.site.register(Invoice, InvoiceAdmin)


class InvoiceItemAdmin(admin.ModelAdmin):
	pass
admin.site.register(InvoiceItem, InvoiceItemAdmin)


class TransactionAdmin(admin.ModelAdmin):
	pass
admin.site.register(Transaction, TransactionAdmin)

