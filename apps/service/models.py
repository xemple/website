from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
import datetime



class Node(models.Model):
	name		=	models.CharField(max_length=100)
	ip			=	models.IPAddressField(null=True, blank=True)
	cpu			=	models.FloatField()
	ram			=	models.FloatField()
	disk_space	=	models.FloatField()
	is_active	=	models.BooleanField()
	
	class Meta:
		verbose_name = _('node')
		verbose_name_plural = _('nodes')
		
	def __unicode__(self):
		return str(self.name)





class Service(models.Model):
	node		=	models.ForeignKey(Node, related_name='node_service')
	name		=	models.CharField(max_length=100)
	ip			=	models.IPAddressField(null=True, blank=True)
	cpu			=	models.FloatField()
	ram			=	models.FloatField()
	disk_space	=	models.FloatField()
	is_active	=	models.BooleanField()
	
	class Meta:
		verbose_name = _('service')
		verbose_name_plural = _('services')
		
	def __unicode__(self):
		return str(self.name)