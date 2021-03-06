import webapp2
from handlers import *

PAGE_RE = '(/(?:[a-zA-Z0-9_-]+/?)*)'
application = webapp2.WSGIApplication([
    (r'^/signup/?$', SignupHandler),
    (r'^/login/?$', LoginHandler),
    (r'^/logout/?$', LogoutHandler),
    (r'/_edit'+PAGE_RE, EditHandler),
    (r'/_history'+PAGE_RE, HistoryHandler),
    (r'^(/(?:[a-zA-Z0-9_-]+/?)*)(\.json)?$', PageHandler),
    ], debug=True)