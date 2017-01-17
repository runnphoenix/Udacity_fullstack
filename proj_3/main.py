import os
import re
import jinja2
import webapp2
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)
    
    
### Handler
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    
    def render(self, template, **kw):
        self.write(render_str(template, **kw))
 
### MainPage   
class MainPage(Handler):
    def get(self):
        self.write('Hello, Full Stack Nanodegree!')
        
### User Account
class Signup(Handler):
    def get(self):
        self.render("signup.html")
    
    def post(self):
        userName = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        
        has_error = False
        params = dict(username = userName, email = email)
        
        if not self.username_valid(userName):
            params['error_username'] = "Not a valid user name."
            has_error = True
            
        if not self.password_valid(password):
            params['error_password'] = "Not a valid password."
            has_error = True
        elif password != verify:
            params['error_verify'] = "Passwords don't match."
            has_error = True
            
        if email and (not self.email_valid(email)):
            params['error_email'] = "Not a valid email."
            has_error = True
            
        if has_error:
            self.render("signup.html", **params)
        else:
            self.write("Signup done.")
        
    # Judge username etc
    def username_valid(self, name):
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        return USER_RE.match(name)
    
    def password_valid(self, password):
        PSWD_RE = re.compile(r"^.{3,20}$")
        return PSWD_RE.match(password)
    
    def email_valid(self, email):
        EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
        return EMAIL_RE.match(email)
        
class Login(Handler):
    def get(self):
        self.render("login.html")
        
class Logout(Handler):
    def get(self):
        self.write("logout")

### Blogs
def blogs_key(name = "default"):
    return db.Key.from_path("blogs", name)
    
class Blogs(Handler):
    def get(self):
        # Show blogs
        blogs = db.GqlQuery("select * from Blog order by created desc limit 10")
        self.render("blogs.html", blogs = blogs)
        
class NewPost(Handler):
    def get(self):
        self.render("newpost.html")
    
    def post(self):
        blogTitle = self.request.get("subject")
        blogContent = self.request.get("content")
        
        # Judge title and content
        errorMessage = self.erMessage(blogTitle, blogContent)
        if errorMessage:
            self.render("newpost.html", errorMessage = errorMessage, blogTitle = blogTitle, blogContent = blogContent)
        else:
            # write db
            blog = Blog(parent = blogs_key(), title = blogTitle, content = blogContent)
            blog.put()
            # goto blog page
            self.redirect("/blog/%s" % str(blog.key().id()))
    
    def erMessage(self, blogTitle, blogContent):
        if blogTitle and (not blogContent):
            return "Content is empty"
        elif (not blogTitle) and blogContent:
            return "Title is empty"
        elif (not blogTitle) and (not blogContent):
            return "Both title and content empty"
        else:
            return None
            
class BlogPage(Handler):
    def get(self, blog_id):
        key = db.Key.from_path("Blog", int(blog_id), parent = blogs_key())
        blog = db.get(key)
        
        if not blog:
            self.error(404)
            return
        
        blog.prepare_render()
        self.render("blogPost.html", blog = blog)
            
class Blog(db.Model):
    title = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    modified = db.DateTimeProperty(auto_now = True)
    
    def prepare_render(self):
        self.content = self.content.replace('\n', '<br>')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/signup', Signup),
    ('/login', Login),
    ('/logout', Logout),
    ('/blog/?', Blogs),
    ('/blog/([0-9]+)', BlogPage),
    ('/blog/newpost', NewPost)
], debug=True)
