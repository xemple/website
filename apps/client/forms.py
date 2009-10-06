from django import forms
from apps.client.models import Client, Contact


class ClientForm(forms.ModelForm):
	class Meta:
		model = Client
		fields = ['email', 'first_name', 'last_name', 'company', 'address', 'city', 'zip_code', 'country']
		
		
		
class ContactForm(forms.ModelForm):
	class Meta:
		model = Contact
		
		
		
class NewClientForm(ClientForm):
	phone 		= 	forms.CharField(max_length=100)
	fax 		= 	forms.CharField(max_length=100)
	cellphone	= 	forms.CharField(max_length=100)
	
	
	class Meta(ClientForm.Meta):
		pass
		
		
	def clean_email(self):
		try:
			user = Client.objects.get(email__exact=self.cleaned_data['email'])
		except Client.DoesNotExist:
			return self.cleaned_data['email']
		raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
		
		
	def save(self):
		new_client = Client.objects.create_client(
													email 		=	self.cleaned_data['email'], 
													first_name	=	self.cleaned_data['first_name'], 
													last_name	=	self.cleaned_data['last_name'], 
													company		=	self.cleaned_data['company'], 
													address		=	self.cleaned_data['address'], 
													zip_code	=	self.cleaned_data['zip_code'], 
													city		=	self.cleaned_data['city'], 
													country		=	self.cleaned_data['country']
													)
		client, username, password = new_client
		new_contact = Contact.objects.create_client_contact(
															client, 
															phone 		= 	self.cleaned_data['phone'],
															fax			=	self.cleaned_data['fax'],
															cellphone	=	self.cleaned_data['cellphone'],
															)
		return client, username, password