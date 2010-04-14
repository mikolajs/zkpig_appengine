# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import os.path

import database

class SchoolHandler(webapp.RequestHandler):
  
  def get(self):
    self.answer()
  
  def post(self):
    self.answer()
  
  def answer(self):
    pageId = self.request.get('id')
    path = 'templates/'
    if (pageId == '' or pageId == None):
      pageId = 'kontakt'
    path = path + pageId.strip()
    path = path + '.html'
    path = os.path.join(os.path.dirname(__file__), path)
    content = file(path,'r').read()
    page_content = {'content':content}
    self.response.out.write(template.render('templates/SCHOOL.HTML', page_content))
    
      