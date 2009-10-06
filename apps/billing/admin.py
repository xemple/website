from django.contrib import admin
from apps.billing.models import Offer, Subscription, Quote, QuoteItem


class OfferAdmin(admin.ModelAdmin):
	list_display = ('name', 'price')


class SubscriptionAdmin(admin.ModelAdmin):
	list_display = ('service', 'smart_time_left')


class QuoteAdmin(admin.ModelAdmin):
	pass


class QuoteItemAdmin(admin.ModelAdmin):
	pass
	
	

admin.site.register(Offer, OfferAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Quote, QuoteAdmin)
admin.site.register(QuoteItem, QuoteItemAdmin)