import os
import logging
import string
import datetime
import jinja2

from google.appengine.ext import db
from google.appengine.api import memcache
import utils as Util

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

def users_key(group = 'default'):
  return db.Key.from_path('users', group)

class WikiUser(db.Model):
  username = db.StringProperty(required=True)
  pw_hash = db.StringProperty(required=True)
  email = db.EmailProperty(required=False)

  def set_user_caches(self):
    Util.set_cache(self.username, self)
    Util.set_cache(str(self.key().id()), self)

  @classmethod
  def by_id(self, uid):
    logging.error('DB QUERY')
    return self.get_by_id(long(uid), parent = users_key())
  @classmethod
  def by_username(self, username):
    logging.error('DB QUERY')
    return self.all().ancestor(users_key()).filter('username = ',username).get()
  @classmethod
  def get_user(self, uid_or_username):
    user = memcache.get(uid_or_username)
    if not user:
      if uid_or_username.isdigit():
        user = self.by_id(uid_or_username)
      else:
        user = self.by_username(uid_or_username)
      if user:
        user.set_user_caches()
    return user
  @classmethod
  def register(self, username, password, email=None):
    pw_hash = Util.make_password_hash(username, password)
    if email:
      return self(parent=users_key(),
          username = username,
          pw_hash = pw_hash,
          email = email)
    else:
      return self(parent=users_key(),
          username = username,
          pw_hash = pw_hash)

  @classmethod
  def validate_login(self, username, password):
    user = self.get_user(username)
    if user and validate_password(username, password, user.pw_hash):
      return user

def render_str(template_path, **params):
  t = jinja_env.get_tempalte(template_path)
  return t.render(params)

def page_key(name='default'):
  return db.Key.from_path('pages', name)

class WikiPage(db.Model):
  content = db.ListProperty(db.Text, required=True)
  created = db.DateTimeProperty(auto_now_add=True)
  date_modified = db.ListProperty(datetime.datetime)

  def render_content(self, version):
    self._render_text = self.content[version - 1].replace('\n', '<br>')
    return render_str('content.html', wiki_page=self)

  def make_dict(self, version):
    d = {"content": self.content[version - 1],
      "created": self.created.strftime("%c"),
      "last_modified": self.date_modified[version - 1].strftime("%c"),
      "page_path": self.key().name()}
    return d
  def update(self, content):
    date_mod = datetime.datetime.now()
    self.content.append(db.Text(content))
    self.date_modified.append(date_mod)
    return self

  @classmethod
  def get_page(self, page):
    wiki_page = memcache.get(page)
    if not wiki_page:
      wiki_page = self.by_page_key(page)
      if wiki_page:
        set_cache(page, wiki_page)
    return wiki_page
  @classmethod
  def by_page_key(self, page):
    logging.error('DB query page-key')
    wiki_page = self.get_by_key_name(page, parent=page_key())
    return wiki_page

  @classmethod
  def construct(self, content, page):
    date_mod = datetime.datetime.now()
    return self(parent=page_key(),
        content = [db.Text(content)],
        date_modified = [date_mod],
        key_name = page)
