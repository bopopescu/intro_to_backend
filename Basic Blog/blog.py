import os
import re
import jinja2 
import webapp2
from string import letters

from google.appengine.ext import db

# Initialize jinja2
template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), 
                               autoescape = True) # Escape Templates
def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)
        
    def render_str(self, template, **params):
        return render_str(template, **params)
    
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

        
class MainPage(Handler):
#    def render_front(self, title="", art="", error=""):
#        # GQL Query
#        arts = db.GqlQuery("SELECT * FROM Art "
#                          "ORDER BY created DESC")
#        
#        self.render("front.html", title= title, art = art, error = error, arts = arts)
#    
    def get(self):
        self.write('Hello, Udacity!')
    
#    def post(self):
#        title = self.request.get("title")
#        art = self.request.get("art")
#        
#        if title and art:
#            a = Art(title = title, art = art) #Create an art instance
#            a.put() # store the instance a in the database
#            
#            self.redirect("/") # redirect to frontpage
#        else:
#            error = "We need both a title and some artworks!"
#            self.render_front(title, art, error)

##### Blog ####
def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

# Google App Engine Datastore
# Define an Entity, add the blog oist submitting by users to the database
class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
    
    def render(self):
        #replace new lines in the input html into line breaks
        self._render_text = self.content.replace('\n','<br>')
        return render_str('post.html', p = self)

class BlogFront(Handler):
    def get(self):
        #posts = Post.all().order('-created')
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 10")
        self.render('front.html', posts = posts)

class PostPage(Handler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent = blog_key())
        post = db.get(key)
        
        if not post:
            self.error(404)
            return
        
        self.render('permalink.html', post = post)

class NewPost(Handler):
    def get(self):
        self.render('newpost.html')
    
    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')
        
        if subject and content:
            p = Post(parent = blog_key(), subject = subject, content = content)
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "Subject and content, please"
            seld.render('newpost.html', subject = subject, content = content)
            
# URL mapping handler
app = webapp2.WSGIApplication([ ('/', MainPage),
                                ('/blog/?', BlogFront),
                                ('/blog/([0-9]+)', PostPage),
                                ('/blog/newpost', NewPost)
                                ],
                                debug=True)
