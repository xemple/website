import datetime
from django.conf import settings
from django.db import models, transaction
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from apps.client.models import Client




class LogManager(models.Manager):
	def log_event(self, client, action, item, ip):
		content_type = ContentType.objects.get_for_model(item)
		object_id = item.id
		now = datetime.datetime.now()
		new_log = self.model(None, client=client, action=action, content_type=content_type, object_id=object_id, timestamp=now, ip_address=ip)
		new_log.save()

class Log(models.Model):
	client			=	models.ForeignKey(User)
	action			=	models.CharField(max_length=200)
	content_type	=	models.ForeignKey(ContentType)
	object_id		=	models.PositiveIntegerField()
	target			=	generic.GenericForeignKey('content_type', 'object_id')
	timestamp		=	models.DateTimeField()
	ip_address		=	models.IPAddressField()
	objects			=	LogManager()