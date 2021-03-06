import os
import jinja2
import webapp2

# Initialize jinja2
template_dir = os.path.join(os.path.dirname(__file__),'templates') #current directoy/templates
jinja_env = jinja2.Environment( loader = jinja2.FileSystemLoader(template_dir), autoescape = True) # Escape  autoescape = True

# form_html = """
#    <form>
#        <h2>Add a Food</h2>
#        <input type="text" name="food">
#        %s
#        <button>Add</button>
#    </form>
# """
#
# hidden_html ="""
#    <input type="hidden" name="food" value="%s">
# """
#
# item_html = "<li>%s</li>"
#
# shopping_list_html = """
#    <br>
#    <br>
#    <h2>Shopping List</h2>
#    <ul>
#        %s
#    </ul>
# """

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class MainPage(Handler):
    def get(self):
        #self.write(form_html)

        # output= form_html
        # output_hidden = ""
        #
        # items = self.request.get_all("food")
        # if items:
        #     output_items = ""
        #     for item in items:
        #         output_hidden += hidden_html % item
        #         output_items += item_html % item
        #
        #     output_shopping = shopping_list_html % output_items
        #     output += output_shopping
        #
        # output = output % output_hidden
        # self.write(output)
        items = self.request.get_all("food")
        self.render("shopping_list.html", name= "Theresa", items = items)

# FizzBuzz
class FizzBuzzHandler(Handler):
    def get(self):
        q = self.request.get('q', 0) # q default 0
        if q:
            q = int(q)
        #q = q and int(q)
        self.render('fizzbuzz.html', q = q)

# URL mapping handler
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/fizzbuzz', FizzBuzzHandler)],
    debug=True)
