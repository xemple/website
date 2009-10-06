# -*- coding: utf-8 -*-
import datetime
from django.conf import settings
from django.db import models, transaction
from django.contrib.auth.models import User





class DnsDomain(models.Model):
	domain			=	models.CharField(max_length=200)
	user			=	models.ForeignKey(User, related_name='user_domain')

	
	
class DnsZone(models.Model):
	domain			=	models.ForeignKey(DnsDomain, related_name='domain_zone')
	data			=	models.CharField(max_length=100)
