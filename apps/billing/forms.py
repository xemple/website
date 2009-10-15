# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _

attrs_dict = { 'class': 'required' }

class VerifyInvoiceCheck(forms.Form):

	tos =			forms.BooleanField(
									widget=forms.CheckboxInput(attrs=attrs_dict), 
									label=_(u'Generate an Invoice and pay it')
									)

	def clean_tos(self):
		"""
		Form : ToS Acceptance
		
		"""
		if self.cleaned_data.get('tos', False):
			return self.cleaned_data['tos']
		raise forms.ValidationError(_(u'You must agree to continue'))