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
    def write(self, *a, **kw):
        self.response.write(*a, **kw)
        
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

#Username: "^[a-zA-Z0-9_-]{3,20}$"
#Password: "^.{3,20}$"
#Email: "^[\S]+@[\S]+.[\S]+$"
        
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Signup(Handler):
    def get(self):
        self.render("signup.html")
        
    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = dict (username = username, email = email)
        
        if not valid_username(username):
            params['error_username'] = "Thast's not a valid username"
            have_error = True
            
        if not valid_password(password):
            params['error_password'] = "Thant's not a valid password"
            have_error = True
            
        elif password != verify:
            params['error_verify'] = "Your password didn't match"
            have_error = True
            
        if not valid_email(email):
            params['error_email'] = "That's not a valid email"
            have_error = True
            
        if have_error:
            self.render('signup.html', **params)
        else:
            self.redirect('/unit2/welcome?username=' + username )
    
class Welcome(Handler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.render('welcome.html', username = username)
        else:
            self.redirect('unit2/signup')    
        
            # URL mapping handler
app = webapp2.WSGIApplication([
    ('/unit2/signup', Signup),
    ('/unit2/welcome', Welcome)],
    debug=True)
