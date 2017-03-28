# -*- coding: utf-8 -*-
import webapp2

# """ to enter longer string
form="""
<form method="get" action="http://www.google.com/search">
   <input name="q">
   <input type="submit">
</form>
"""

class MainPage(webapp2.RequestHandler):
    def get(self):
        #self.response.headers['Content­Type'] = 'text/plain' #dfault html
        self.response.write(form)

# URL mapping handler
app = webapp2.WSGIApplication([('/', MainPage),], debug=True)
