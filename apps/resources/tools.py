from django.utils.encoding import smart_str
from django.utils.hashcompat import md5_constructor, sha_constructor
from django.contrib.auth.models import User
from django import http
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context
import ho.pisa as pisa
import cStringIO as StringIO
import cgi
#TEST
from apps.support.models import Ticket






#		   .
#		  / \
#		/  |  \
#	  /	   |	\		WORK IN PROGRESS
#	/	   o	  \	  
# /_________________\


def xemple_username_generator(fn, ln):
	fn, ln =fn.strip(), ln.strip()
	first_letters = '%s%s' % (fn[:1], ln[:1])
	p1 = first_letters.upper()
	total_user = User.objects.count()
	user_number = total_user+1
	username = '%s%s_xemple' % (p1, user_number)
	return '%s' % username
	
	

def get_hexdigest(algorithm, salt, raw_password):
	raw_password, salt = smart_str(raw_password), smart_str(salt)
	if algorithm == 'crypt':
		try:
			import crypt
		except ImportError:
			raise ValueError('"crypt" password algorithm not supported in this environment')
		return crypt.crypt(raw_password, salt)

	if algorithm == 'md5':
		return md5_constructor(salt + raw_password).hexdigest()
	elif algorithm == 'sha1':
		return sha_constructor(salt + raw_password).hexdigest()
	raise ValueError("Got unknown password algorithm type in password.")



def check_password(raw_password, enc_password):
	algo, salt, hsh = enc_password.split('$')
	return hsh == get_hexdigest(algo, salt, raw_password)


def make_random_password(length=10, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'):
	from random import choice
	return ''.join([choice(allowed_chars) for i in range(length)])


def vat_rate_check(user):
	pass

def calculate_vat(amount):
	vat_rate = float(19.6)
	vat = float(amount)/int(100)*vat_rate
	return vat_rate, vat

def calculate_billing(user, item, quantity):
	total_wot = float(item.price)*int(quantity)
	vat_rate, vat = calculate_vat(total_wot)
	total_ti = total_wot+vat
	return item.price, quantity, total_wot, vat_rate, round(vat,2), round(total_ti,2)

def download_in_pdf(request):
	if request.POST:
		result = StringIO.StringIO()
		pdf = pisa.CreatePDF(
			StringIO.StringIO(request.POST["data"]),
			result
			)

		if not pdf.err:
			return http.HttpResponse(
				result.getvalue(),
				mimetype='application/pdf')

	return http.HttpResponse('We had some errors')

def render_to_pdf(template_src, context_dict):
	
	template = get_template(template_src)
	context = Context(context_dict)
	html  = template.render(context)
	result = StringIO.StringIO()
	pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return http.HttpResponse(result.getvalue(), mimetype='application/pdf')
	return http.HttpResponse('We had some errors<pre>%s</pre>' % cgi.escape(html))
	
	
def pdf_test(request):
	source	= Ticket.objects.get(id=1)
	template = 'support/test_pdf.html'
	render_to_pdf(template, source)
