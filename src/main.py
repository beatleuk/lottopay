"""Syndicate Lotto Payments Page"""

# standard library imports
import os
import time

# third-party imports
import webapp2
import jinja2
import jwt

# application-specific imports
from sellerinfo import SELLER_ID
from sellerinfo import SELLER_SECRET

jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/templates'))

class MainHandler(webapp2.RequestHandler):
  """Handles /"""

  def get(self):
    """Handles get requests."""

    curr_time = int(time.time())
    exp_time = curr_time + 3600

    request_info = {'currencyCode': 'GBP',
                    'sellerData': 'Custom Data'}
    jwt_info = {'iss': SELLER_ID,
                'aud': 'Google',
                'typ': 'google/payments/inapp/item/v1',
                'iat': curr_time,
                'exp': exp_time,
                'request': request_info}

    # create JWT for first item
    request_info.update({'name': 'Euro Millions single draw entry', 'price': '2.11'})
    token_1 = jwt.encode(jwt_info, SELLER_SECRET)

    # create JWT for second item
    request_info.update({'name': 'Euro Millions bank 10 pounds', 'price': '10.53'})
    token_2 = jwt.encode(jwt_info, SELLER_SECRET)

    # create JWT for third item
    request_info.update({'name': 'Euro Millions bank 20 pounds', 'price': '21.05'})
    token_3 = jwt.encode(jwt_info, SELLER_SECRET)

    # update store web page
    template_vals = {'jwt_1': token_1,
                     'jwt_2': token_2,
                     'jwt_3': token_3}

    template_path = 'index.html'
    template = jinja_environment.get_template(template_path)
    self.response.out.write(template.render(template_vals))

class PostbackHandler(webapp2.RequestHandler):
  """Handles server postback - received at /postback"""

  def post(self):
    """Handles post request."""
    encoded_jwt = self.request.get('jwt', None)
    if encoded_jwt is not None:
      # jwt.decode won't accept unicode, cast to str
      # http://github.com/progrium/pyjwt/issues/4
      decoded_jwt = jwt.decode(str(encoded_jwt), SELLER_SECRET)

      # validate the payment request and respond back to Google
      if decoded_jwt['iss'] == 'Google' and decoded_jwt['aud'] == SELLER_ID:
        if ('response' in decoded_jwt and
            'orderId' in decoded_jwt['response'] and
            'request' in decoded_jwt):
          order_id = decoded_jwt['response']['orderId']
          request_info = decoded_jwt['request']
          if ('currencyCode' in request_info and 'sellerData' in request_info
              and 'name' in request_info and 'price' in request_info):
            # optional - update local database
            
            # respond back to complete payment
            self.response.out.write(order_id)


routes = [webapp2.Route('/', MainHandler),
          webapp2.Route('/postback', PostbackHandler)]

app = webapp2.WSGIApplication(routes, debug=True)

