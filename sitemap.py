# -*- coding: utf-8 -*-



# AppEngine
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

# Cruise Control
#from handlers import admin

class sitemapHandler(webapp.RequestHandler):
  def get(self):
    #tu dodać sprawdzenie adresu pobranego
    page = self.request.url.split("/")[-1]
    if page == "sitemap.xml":
      f = file("templates/sitemap.xml","r")
      self.response.out.write(f.read())
    else:
      self.response.out.write("User-agent: * \nAllow: /")
      self.response.out.write("")

HANDLERS = [('/sitemap', sitemapHandler),
            ('/sitemap.xml',  sitemapHandler),
            ('/robots.txt', sitemapHandler)]
            
def main():
  # NOTE: Set debug to True when pushing to testing changes
  application = webapp.WSGIApplication(HANDLERS, debug=True)
  run_wsgi_app(application)

if __name__ == "__main__":
  main()