# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users

import os.path

import database

class LoginHandler(webapp.RequestHandler):
  
  def get(self):
    self.login()

  def post(self):
    self.login()
    
  
  def login(self):
    action = self.request.get('action')
    fromPage = self.request.get('from')
    returnPath = os.path.split(self.request.uri)[0]
    if fromPage == "news":
      returnPath += "/news"
    else:
      returnPath += "/parents"
    if action == "zaloguj":
      self.redirect(users.create_login_url(returnPath))
    else:
      self.redirect(users.create_logout_url(returnPath))
    
  
