# Copyright 2012 Google Inc. All Rights Reserved.

# pylint: disable-msg=C6409,C6203

"""In-App Payments - Online Store Python Sample"""

# standard library imports
from cgi import escape
import os
import time

# third-party imports
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
import jwt

# application-specific imports
from sellerinfo import SELLER_ID
from sellerinfo import SELLER_SECRET

class MainHandler(webapp.RequestHandler):
  """Handles /"""

  def get(self):
    """Handles get requests."""

    # TODO: Implement JWT generation for token_1 and token_2
    token_1 = '';
    token_2 = '';

    # update store web page
    template_vals = {'jwt_1': token_1,
                     'jwt_2': token_2}

    path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
    self.response.out.write(template.render(path, template_vals))


class PostbackHandler(webapp.RequestHandler):
  """Handles server postback - received at /postback"""

  def post(self):
    """Handles post request."""
    
    # TODO: Implement postback handling


application = webapp.WSGIApplication([
    ('/', MainHandler),
    ('/postback', PostbackHandler),
], debug=True)


def main():
  run_wsgi_app(application)


if __name__ == '__main__':
  main()
