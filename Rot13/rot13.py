import os
import re
from string import letters

import jinja2
import webapp2

from google.appengine.ext import db

# Initialize jinja2
template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape = True) # Escape Templates


class Handler(webapp2.RequestHandler):
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.write(*a, **kw)

class Rot13(Handler):
    def get(self):
        self.render("rot13.html")

    def post(self):
        rot13 = ""
        text = self.request.get('text')
        if text:
            rot13 = text.encode('rot13')
        self.render('rot13.html', text = rot13)

# URL mapping handler
app = webapp2.WSGIApplication([
    ('/unit2/rot13', Rot13)],
    debug=True)
