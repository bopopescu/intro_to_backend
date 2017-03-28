# -*- coding: utf-8 -*-
import webapp2

# form="""
# <form action="/testform">
#    <input name="q">
#    <input type="submit">
# </form>
# """

form="""
<form method="post" action="/testform">
   <input name="q">
   <input type="submit">
</form>
"""

class MainPage(webapp2.RequestHandler):
   def get(self):
       self.response.write(form)

# GET method for TestHandler
# class TestHandler(webapp2.RequestHandler):
#    def get(self):
#        q = self.request.get("q") # request sent from the browser
#        self.response.out.write(q) # response sent back to the client
#         # self.response.headers['Content-Type'] = 'text/plain'
#         # self.response.out.write(self.request)

# POST method for TestHandler
class TestHandler(webapp2.RequestHandler):
   def post(self):
    #    q = self.request.get("q") # request sent from the browser
    #    self.response.out.write(q) # response sent back to the client
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(self.request)

# URL mapping handler
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/testform', TestHandler)],
    debug=True)
