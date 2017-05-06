import os
import jinja2
import webapp2
import urllib2
import json
from xml.dom import minidom
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

# from xml.dom import minidom
# def get_coords(xml):
    # d = minidom.parseString(xml)
    # coords = d.getElementsByTagName("gml:coordinates")
    # if coords and coords[0].childNodes[0].nodeValue:
    #     lon, lat = coords[0].childNodes[0].nodeValue.split(',')
    #     return lon, lat

# print get_coords(xml)

#  IP_URL = "http://api.hostip.info/?ip="
IP_URL = "http://freegeoip.net/json/"
# Request ip --> coordinates
def get_coords(ip):
    ip = "4.2.2.2"
    ip = "23.24.209.141"
    url = IP_URL + ip
    content = None
    try:
        content = urllib2.urlopen(url).read()
    except URLError:
        return

    if content:
        ## parse json
        d = json.loads(content)
        lat = d['latitude']
        lon = d['longitude']
        print lat, lon
        if lat and lon:
            return db.GeoPt(lat, lon)

        # # parse XML
        # d = minidom.parseString(content)
        # coords = d.getElementsByTagName("gml:coordinates")
        # if coords and coords[0].childNodes[0].nodeValue:
        #     lon, lat = coords[0].childNodes[0].nodeValue.split(',')
        #     return db.GeoPt(lat, lon)

# Get GMAP_URL based on the coords
GMAPS_URL = "https://maps.googleapis.com/maps/api/staticmap?size=380x263&"
KEY = "&key=AIzaSyB8MxnS__tiLkJeg05_njxXUwKqbyCwtIk"
def gmaps_img(points):
    markers = '&'.join('markers=%s,%s' % (point.lat, point.lon) for point in points)
    return GMAPS_URL + markers + KEY

# Google App Engine Datastore
# Define an Entity, add the artworks submitting by users to the database
class Art(db.Model):
    title = db.StringProperty(required = True)  # string < 500 chars, indexed
    art = db.TextProperty(required = True)      # text  > 500 chars, not indexed
    created = db.DateTimeProperty(auto_now_add = True)
    coords = db.GeoPtProperty()

# Template
class MainPage(Handler):
    def render_front(self, title="", art="", error=""):
        # GQL Query
        arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC LIMIT 10")
        arts = list(arts) # Cache the result of the queries

        # Find which arts have coords
        points = filter(None, (art.coords for art in arts))
        # points = []
        # for art in arts:
        #     if art.coords:
        #         points.append(art.coords)

        # if we have any arts coords, make an imgae url
        # display the image url
        img_url = None
        if points:
            img_url = gmaps_img(points)

        self.render("front.html", title = title, art = art, error = error, arts = arts, img_url = img_url)


    def get(self):
        # self.write("ascii chan!")
        # self.render("front.html")
        # self.write(self.request.remote_addr)
        # self.write(repr(get_coords(self.request.remote_addr)))
        self.render_front()

    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")

        if title and art:
            # self.write("Thanks!")
            a = Art(title = title, art = art) #Create an art instance
            # Lookup the user's coordinates from their IP
            coords = get_coords(self.request.remote_addr)
            # if we have coordinates, add them to the Art
            if coords:
                a.coords = coords
            a.put() # store the instance a in the database

            self.redirect("/") # redirect to frontpage
        else:
            error = "We need both a title and some artworks!"
            # self.render("front.html", error = error)
            self.render_front(title, art, error)

# URL mapping handler
app = webapp2.WSGIApplication([
    ('/', MainPage)],
    debug=True)
