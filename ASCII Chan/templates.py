import os
import jinja2 
import webapp2
from google.appengine.ext import db

# Initialize jinja2
template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), 
                               autoescape = True) # Escape Templates

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)
        
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

# Google App Engine Datastore
# Define an Entity, add the artworks submitting by users to the database
class Art(db.Model):
    title = db.StringProperty(required = True)
    art = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
        
# Template        
class MainPage(Handler):
    def render_front(self, title="", art="", error=""):
        # GQL Query
        arts = db.GqlQuery("SELECT * FROM Art "
                          "ORDER BY created DESC")
        
        self.render("front.html", title= title, art = art, error = error, arts = arts)
    
    def get(self):
        self.render_front()
    
    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")
        
        if title and art:
            #self.write("Thanks!")
            a = Art(title = title, art = art) #Create an art instance
            a.put() # store the instance a in the database
            
            self.redirect("/") # redirect to frontpage
        else:
            error = "We need both a title and some artworks!"
            self.render_front(title, art, error)
            
# URL mapping handler
app = webapp2.WSGIApplication([
    ('/', MainPage)],
    debug=True)
