import webapp2

# String substitution
# "<b>%s</br>" %VAR
# "text%stext%s" %(VAR1, VAR2)
# "text%(NAME)s"  % {"NAME": VALUE}

form="""
<form method="post">
    What is your birthday?
    <br>
    <label> Month
        <input type="text" name="month" value="%(month)s">
    </label>
    <label> Day
        <input type="text" name="day" value="%(day)s">
    </label>
    <label> Year
        <input type="text" name="year" value="%(year)s">
    </label>
    <div style="color: red">%(error)s</div>
    <br>
    <br>
    <input type="submit">
</form>
"""

class MainPage(webapp2.RequestHandler):
    def write_form(self, error="", month="", day="", year=""):
        self.response.write(form % { "error": error,
                                    "month": escape_html(month),
                                    "day": escape_html(day),
                                    "year": escape_html(year)})

    # GET handler to draw the form
    def get(self):
        #self.response.write(form)
        self.write_form()

    # POST handler to post the form
    def post(self):
        # User inputs
        user_month = self.request.get('month')
        user_day = self.request.get('day')
        user_year = self.request.get('year')

        month = valid_month(user_month)
        day = valid_day(user_day)
        year = valid_year(user_year)

        # (1) Verify the user's input
        # (2) On error, rerender form again
        # (3) Include error messages
        if not (month and day and year):
            #self.response.write(form)
            #self.write_form("That does not look valid!")
            self.write_form("Day is not valid!", user_month, user_day, user_year)
        else:
            #self.response.write("Thanks! That's a valid day")
            self.redirect("/thanks")

# Redirecting
class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("Thanks! It's a valid day!")

# URL mapping handler
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/thanks', ThanksHandler)],
    debug=True)


#Validate Month
months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']

# Month dictionary...
# {
#  "Mar": "March",
#  "Feb": "February",
#  "Aug": "August",
#  "Sep": "September"
# }
month_abbv = dict((m[:3].capitalize() , m) for m in months)

def valid_month(month):
    if month:
        cap_month = month.capitalize()
        short_month =  cap_month[:3]

        if cap_month in months:
           return cap_month

        elif short_month in month_abbv:
            return month_abbv.get(short_month)

#Validate Day
def valid_day(day):
    if day and day.isdigit():
        day = int(day)
        if day in range(1,32):
            return day

#Validate Year
def valid_year(year):
    if year and year.isdigit():
        year = int(year)
        if year in range(1900, 2021):
            return year

# HTML Escaping
# "  &quot;
# >  &gt;
# <  &lt;
# &  &amp;
import cgi
def escape_html(s):
    return cgi.escape(s, quote = True)
    # for i, o in [ ("&" , "&amp;"), (">", "&gt;"), ("<", "&lt;"), ('"', "&quot;")]:
    #     s = s.replace(i, o)
    # return s
