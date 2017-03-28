# -*- coding: utf-8 -*-
import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content­Type'] = 'text/plain' #dfault html
        self.response.write('Hello, World!')

# URL mapping handler
app = webapp2.WSGIApplication([
    ('/', MainPage),], debug=True)
