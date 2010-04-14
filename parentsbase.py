# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users

import database

class ParentsBase(webapp.RequestHandler):
  """postawa dla handlerów Parents, zapewnia menu boczne dodawane do HTML jako znacznik {{menu}}"""
  def __init__(self):
    self.page_content = {}
  
  
  
  def makeMenu(self):
    """musi zostać uruchomiona w obiekcie dziecka"""
    username = 'anonimowy'
    loginfo = 'zaloguj'
    departments = database.Department.all()
    user = users.get_current_user()
    if user:
      username = user.email()
      loginfo = 'wyloguj'
    page_content = {}
    page_content['loginfo'] = loginfo
    page_content['username'] = username
    page_content['showcreate'] = False
    if self.isEditor(username):
      page_content['showcreate'] = True
      #ładowanie postów
    page_content['posts'] = database.ParentsPost.all()
    self.page_content['menu'] = template.render('templates/parentsnewsmenu.html', page_content)
    
    
  def isEditor(self, mail):
    if mail == 'radarodzicow.zkpig26gdansk@gmail.com' or mail == 'mikolajsochacki@gmail.com':
      return True
    return False
