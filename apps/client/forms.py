from django import forms
from django.contrib.auth.models import User
from apps.client.models import ClientProfile



class NewClientForm(forms.ModelForm):
	first_name		=	forms.CharField(max_length=100)
	last_name		=	forms.CharField(max_length=100)
	email			=	forms.EmailField(max_length=100)	
	
	
	class Meta:
		model = ClientProfile
		exclude = ('user',)
		
		
	def clean_email(self):
		try:
			user = User.objects.get(email__exact=self.cleaned_data['email'])
		except User.DoesNotExist:
			return self.cleaned_data['email']
		raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
		
		
	def save(self):
		new_client = ClientProfile.objects.create_client(
													first_name	=	self.cleaned_data['first_name'], 
													last_name	=	self.cleaned_data['last_name'],
													email		=	self.cleaned_data['email'],	 
													company		=	self.cleaned_data['company'], 
													address		=	self.cleaned_data['address'],
													address_ext	=	self.cleaned_data['address_ext'], 
													zip_code	=	self.cleaned_data['zip_code'], 
													city		=	self.cleaned_data['city'], 
													country		=	self.cleaned_data['country'],
													phone		=	self.cleaned_data['phone'],
													fax			=	self.cleaned_data['fax'],
													cellphone	=	self.cleaned_data['cellphone'],
													)
		return new_client