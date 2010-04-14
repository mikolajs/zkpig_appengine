# -*- coding: utf-8 -*-



from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import db

import os.path

import database
import datetime

class PieceofnewsHandler(webapp.RequestHandler):
  """pokazuje dany news i pozwala wejść do opcji zalogowania,
   jeżeli użytkownik jest autorem postu"""
  def get(self):
      self.show_content()
      
  def post(self):
    self.show_content()
 
       
  def show_content(self):
    """główna metoda wykonywana przy pobraniu"""
    username = "anonimowy"
    departments = database.Department.all()
    keyStr = self.request.get('id')
    key = db.Key(keyStr)
    postsTem = database.Post.gql("WHERE __key__ = :1", key)
    self.post = postsTem.fetch(1)[0]
    user = users.get_current_user()
    self.alter_Images()
    department = self.post.department.department
    page_content = {  'username':username, 'loginfo':'zaloguj', "post":self.post, 'departments': departments, 'showedit':False, 'department': department }
    if user:
      page_content['username'] = user.email()
      page_content['showedit'] = self.isOwner(user.email())
      page_content['loginfo'] = 'wyloguj'
    else:
      page_content['username'] = 'anonimowy'      
    self.response.out.write(template.render('templates/PIECEOFNEWS.HTML', page_content))
    
    
  def isOwner(self, email):
    """Sprawdza czy użytkownik zalogowany jest autorem postu"""
    #authResult = database.Authors.gql('WHERE email = :1',email) #nieprawidłowo - działa dla wszystkich edytorów
    #auth = authResult.fetch(1)
    #if len(auth) > 0:
      #if auth[0].email == email:
    if self.post.author.email == email or email == 'mikolajsochacki@gmail.com':
      return True
    else:
      return False
        
  def alter_Images(self):
    """zmienia tagi [img0] na <img >"""
    tag_imgBegin =  '<img src="img?img_id=%s' % (self.post.key())
    self.post.body = self.post.body.replace('[img1]',tag_imgBegin + '&nr=1" />')
    self.post.body = self.post.body.replace('[img2]',tag_imgBegin + '&nr=2" />')
    self.post.body = self.post.body.replace('[img3]',tag_imgBegin + '&nr=3" />')
    
    