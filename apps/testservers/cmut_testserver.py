from random import choice

def pay(amount):
	length=10 
	allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'
	return True, amount, ''.join([choice(allowed_chars) for i in range(length)])