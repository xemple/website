from django import forms
from django.utils.translation import ugettext as _

attrs_dict = { 'class': 'required' }


class LoginForm(forms.Form):
	username =		forms.CharField(
									 widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=75)),
									 label=_(u'username')
									 )
	password =		forms.CharField(
									widget=forms.PasswordInput(attrs=attrs_dict), 
									label=_(u'password')
									)
