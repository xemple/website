from django.utils.encoding import smart_str
from django.utils.hashcompat import md5_constructor, sha_constructor
from django.contrib.auth.models import User


def xemple_username_generator(fn, ln):
	fn, ln =fn.strip(), ln.strip()
	first_letters = '%s%s' % (fn[:1], ln[:1])
	p1 = first_letters.upper()
	total_user = User.objects.count()
	user_number = total_user+1
	username = '%s-%s@xemple' % (p1, user_number)
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