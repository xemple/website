# -*- coding: utf-8 -*-
import datetime
from django.conf import settings
from django.db import transaction
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from apps.billing.models import Offer, MiniCart, Invoice, Subscription, InvoiceItem, Transaction
from apps.resources.tools import calculate_billing
from apps.billing.forms import VerifyInvoiceCheck
from django.http import HttpResponse
from django.template import loader, Context
from django import http
from django.template.loader import get_template, render_to_string
from apps.emailing.models import XmailTemplate
from django.core.mail import send_mail

def xemple_send_mail(mail_type, context):
	user_context = context['user']
	user = User.objects.get(id=user_context.id)
	xmail_obj = XmailTemplate.objects.get(mail_type=mail_type)
	message = render_to_string(xmail_obj.template, context)
	send_mail(xmail_obj.subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
	return True