from django.db import models
from django.utils.translation import ugettext_lazy as _





class XmailTemplate(models.Model):
	mail_type		=	models.CharField(max_length=50)
	subject			=	models.CharField(max_length=100)
	template		=	models.CharField(max_length=200)
	
	class Meta:
		verbose_name = _('Mail Template')
		verbose_name_plural = _('Mails Templates')
		
	def __unicode__(self):
		return str(self.mail_type)
