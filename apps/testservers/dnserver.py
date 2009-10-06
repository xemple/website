def check_dn_avail(domain, ext):
	li = (ext)
	return domain, li
	
def check_all_avail_ext(domain):
	li = ('.com', '.net', '.org')
	return domain, li

def check_avail_dn_ext(full_domain):
	try:
		domain, ext = full_domain.split('.')
		res = check_dn_avail(domain, ext)
	except ValueError:
		domain = full_domain
		res = check_all_avail_ext(str(domain))
	return res