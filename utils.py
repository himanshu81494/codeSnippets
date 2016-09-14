import random
import string
import re
import hmac
import hashlib
import logging

from google.appengine.api import memcache
  SECRET = 'my secret is SECRET'

def set_cache(cache_key, value):
  client = memcache.Client()
  try:
    while True:
      old_value = client.gets(cache_key)
      assert old_value, 'Uninitialized Key'
      if client.cas(cache_key, value):
        break
  except AssertionError:
    client.add(cache_key, value)
    logging.error('Initializing Key')

def make_salt():
  return ''.join(random.choice(string.letters) for x in xrange(5))

def make_password_hash(name, password, salt = make_salt()):
  h = hashlib.sha256(name + password + salt).hexdigest()
  return '%s,%s'%(h, salt)

def validate_password(name, password, h):
  return h == make_password_hash(name, password, h.split(',')[-1])

def make_hash_str(value):
  return hmac.new(SECRET, val).hexdigest()

def make_cookie(value):
  return '%(value)s|%(hashed)s'%{'value': value, 'hashed': make_hash_str(value)}

def check_cookie(cookiedata):
  value = cookiedata.split('|')[0]
  if cookiedata == make_cookie(value):
    return value
