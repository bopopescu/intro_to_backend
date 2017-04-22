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


##### Blog ####
def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name) # the value of blog's parent

# Post Model
# Google App Engine Datastore. Define an Entity, add the blog post submitting by users to the database
class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

    def render(self):
        #replace new lines in the input html into line breaks
        self._render_text = self.content.replace('\n','<br>')
        return render_str('post.html', p = self)

# '/blogs'
class BlogFront(Handler):
    def get(self):
        #posts = Post.all().order('-created') # Google procedure language
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 10")
        self.render('front.html', posts = posts)

# '/blogs/([0-9]+)'
class PostPage(Handler):
    def get(self, post_id):
        # post = Post.get_by_id(int(post_id))
        # if p:
        #     self.render('permalink.html', post = post)
        key = db.Key.from_path('Post', int(post_id), parent = blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        self.render('permalink.html', post = post)

# '/blogs/newpost'
class NewPost(Handler):
    def get(self):
        self.render('newpost.html')

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Post(parent = blog_key(), subject = subject, content = content) # Create a Post instance p
            p.put() # store the Post instance p in the database
            self.redirect('/blogs/%s' % str(p.key().id()))
        else:
            error = "Subject and content, please"
            seld.render('newpost.html', subject = subject, content = content)

# URL mapping handler
app = webapp2.WSGIApplication([ ('/', BlogFront),
                                ('/blogs/?', BlogFront),
                                ('/blogs/([0-9]+)', PostPage),
                                ('/blogs/newpost', NewPost)
                                ],
                                debug=True)
