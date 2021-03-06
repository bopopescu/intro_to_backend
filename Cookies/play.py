import os
import jinja2
import webapp2
import hashlib
import hmac

SECRET = 'imsosecret'

# Hashing Cookies
def hash_str(s):
    #md5
    # return hashlib.md5(s).hexdigest()
    # return hashlib.sha256(s).hexdigest()
    # HMAC (Hash-based Messaging Authentication Code)
    return hmac.new(SECRET, s).hexdigest()

# make_secure_val, which takes a string and returns a string of the format:
# s,HASH
def make_secure_val(s):
    #return "%s,%s" %(s, hash_str(s))
    return "%s|%s" % (s, hash_str(s))

# check_secure_val, which takes a string of the format
# s,HASH
# and returns s if hash_str(s) == HASH, otherwise None
def check_secure_val(h):
    # s = h.split(",")[0]
    s = h.split("|")[0]
    if h == make_secure_val(s):
        return s

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
        self.response.headers['Content-Type'] = 'text/plain'
        # visits = self.request.cookies.get('visits', '0') # get cookies visit if not set cookies = '0'
        # # make sure visits is an int
        # if visits.isdigit():
        #     visits = int(visits) + 1
        # else:
        #     visits = 0

        visits = 0
        visit_cookie_str = self.request.cookies.get('visits')
        if visit_cookie_str:
            cookie_val = check_secure_val(visit_cookie_str) #  1 | HMAC(SECRET,1)
            if cookie_val:
                visits = int(cookie_val)

        visits += 1
        new_cookie_val = make_secure_val(str(visits)) # 2 | HMAC(SECRET,2)
        self.response.headers.add_header('Set-Cookie', 'visits=%s' % new_cookie_val)
        # self.response.headers.add_header('Set-Cookie', 'visits=%s' % visits)
        # self.write("You've been here %s times!" % visits)

        if visits > 100:
            self.write("You are the best ever!")
        else:
            self.write("You've been here %s times!" % visits)

# URL mapping handler
app = webapp2.WSGIApplication([
    ('/', MainPage)], debug=True)


# Cheat the cookies
# document.cookie
# "visits=23"
# document.cookie="visits=1000"

# Hashing
# H(x) - > y
# x : data
# y : fixed length bit string

# Hash Algorithms
# crc32   - checksums, fast
#         - collision, two things hash to the same value
# md5     - fast, not secure
# sha1    - secure-ish
# sha256  - secure, slow
