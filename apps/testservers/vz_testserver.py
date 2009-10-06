import time
from random import choice

def generate_vz_name(acc_name):
	allowed_chars = 'abcdefjhijklmnopqrstuvwxyz123456789'
	vz_num = ''.join([choice(allowed_chars) for i in range(7)])
	vz_name = '%s_%s' % (acc_name, vz_num)
	print "Generating VZ Container name"
	return vz_name
	 
def generate_ip():
	allowed_chars = '123456789'
	ip_block = ''.join([choice(allowed_chars) for i in range(2)])
	print "Generating IP bloc"
	return ip_block
	
def ip_pool():
	time.sleep(0.3)
	ip = "%s.%s.%s.%s" % (generate_ip, generate_ip, generate_ip, generate_ip)
	print "Generating IP"
	return ip

def create_cube(ram, disk, ip): 
	time.sleep(0.5)
	created = True
	print "Cube is created"
	return created
	
def generate_cube(acc_name, ram, disk):
	time.sleep(0.5)
	ip = ip_pool
	vz_name = generate_vz_name
	create = create_cube(ram=ram, disk=disk, ip=ip)
	print "Cube is now running with a name and an IP address"
	if create == True:
		return True, ram, disk, ip
	else:
		return False
			
def restart_cube():
	print "Cube is restarting"
	time.sleep(3.5)
	print "Cube is now running"
	return True

def stop_cube():
	print "Cube is shuting down"
	time.sleep(1.5)
	print "Cube is now down"
	return True
	
def start_cube():
	print "Cube is starting"
	time.sleep(1.5)
	print "Cube is now running"
	return True

def get_vz_status(vz_id):
	time.sleep(0.5)
	return '50', '78'
	
def get_domain_for_vz(vz_id):
	return 'www.impact-bar.fr'

def deploy_django(vz_id):
	print "Starting to deploy django"
	time.sleep(1.5)
	print "Django is now running on the container"
	return True

def add_vz_ip(vz_id):
	time.sleep(0.5)
	ip = ip_pool
	print "A new IP has been generated"
	return ip