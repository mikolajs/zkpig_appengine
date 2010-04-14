# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.api import images


import os.path

import database
import datetime
import exceptions
import validator



class ArticleHandler(webapp.RequestHandler):
  """Klasa obsługująca dodawanie i edycję artykułów  rady rodziców"""
  def get(self):
    self.show_content()

  def post(self):
    self.getArgum()
    if self.choice == "Zapisz":
      self.make_insert()
    elif self.choice == "Anuluj":
      if self.insert:
        self.redirect('/parentsnews')
      else:
        self.redirect('/parentsnews?&nmb=%s' % (self.id) )
    else:
      if not self.insert:
        self.deletePost()
      self.redirect('/parents')
 
  def show_content(self,  edit_info = "Dodawanie nowej wiadomości."):
    """Wysyła formatkę do edycji lub informację o niemożliwości edycji 
       bez zalogowania"""
    self.getArgum()
    if not self.user:
      self.response.out.write('<html><body><head><meta http-equiv="content-type" content="text/html; charset=utf-8" /></head><h1> Nie jesteś zalogowany. <br/><a href="/news"> Powrót </a> </h1><body/><html/>')
      return #exit()   
    self.getPost()    
    if not self.insert:
      edit_info = 'Poprawianie treści wiadomości'      
    if self.canEdit():
      page_content = {'edit_info':edit_info, 'post':self.post } 
      self.response.out.write(template.render('templates/POSTS.HTML', page_content))  
    else:
      self.response.out.write('<html><body><head><meta http-equiv="content-type" content="text/html; charset=utf-8" /></head><h1> Niestety nie masz uprawnień do tworzenia postów. <br/><a href="/news"> Powrót </a> </h1><body/><html/>')
        
#przerobić tak, żeby używało insert i alter        
  def make_insert(self):
    if not self.user:
      self.response.out.write('<html><body><head><meta http-equiv="content-type" content="text/html; charset=utf-8" /></head><h1> Nie jesteś zalogowany. <br/><a href="/news"> Powrót </a> </h1><body/><html/>')
      return #exit() 
    self.getPost()
    #wspólne dla obu akcji
    self.post.title = self.request.get('title')
    self.post.body = db.Text(self.request.get('body'))
    val = validator.Validator()
    val.validatePost(self.post)
    #dodawanie obrazków - jeżeli nie są puste
    if self.request.get('img0'):
      img0 = self.request.get('img0')
      whatResize = self.check_resize(img0)
      if whatResize is "w":
        img0 = images.resize(img0,width=520)
      elif whatResize is "h":
        img0 = images.resize(img0,height=350)
      if img0:
        self.post.img0 = db.Blob(img0)
    if self.request.get('img1'):
      img1 = self.request.get('img1')
      whatResize = self.check_resize(img1)
      if whatResize is "w":
        img1 = images.resize(img1,width=520)
      elif whatResize is "h":
        img1 = images.resize(img1,height=350)
      if img1:
        self.post.img1 = db.Blob(img1)
    if self.request.get('img2'):
      img2 = self.request.get('img2')
      whatResize = self.check_resize(img2)
      if whatResize is "w":
        img2 = images.resize(img2,width=520)
      elif whatResize is "h":
        img2 = images.resize(img2,height=350)
      if img2:
        self.post.img2 = db.Blob(img2)
    if self.request.get('img3'):
      img3 = self.request.get('img3')
      whatResize = self.check_resize(img3)
      if whatResize is "w":
        img3 = images.resize(img3,width=520)
      elif whatResize is "h":
        img3 = images.resize(img3,height=350)
      if img3:
        self.post.img3 = db.Blob(img3)
    #data
    d = datetime.date.today()
    month = [' stycznia ',' lutego ',' marca ',' kwietnia ',' maja ',' czerwca ',' lipca ',' sierpnia ',' września ',' października ',' listopada ',' grudnia ']
    if self.insert:
      self.post.creation_date = datetime.datetime.utcnow()  
      self.post.creation_dateStr = str(d.day) 
      self.post.creation_dateStr += month[d.month -1]
      self.post.creation_dateStr += str(d.year)
      self.post.edit_dateStr = ""
    self.post.put()
    self.redirect('/parentsnews?&nmb=%s' % (self.post.key()) )
    

 
  def getArgum(self):
    """pobiera parametry - wywoływać na samym początku"""
    self.choice = self.request.get('choice')
    action = self.request.get('action')
    if action == 'insert':
      self.insert = True
    elif action == 'alter':
      self.insert = False
    else:
      raise EnvironmentError, "Incorrect action!" 
    self.id = self.request.get('nmb')
    self.user = users.get_current_user()
 
  def getPost(self):
    """tworzy pole z obiektem Post  - pusty dla nowej wiadomości 
    lub konkretny dla danej wiadomości"""
    if self.insert:
      self.post = database.ParentsPost()
    else:
      key = db.Key(self.id)
      postsTem = database.ParentsPost.gql("WHERE __key__ = :1", key)
      self.post = postsTem.fetch(1)[0]
      val = validator.Validator()
      val.loadPost(self.post)
    
    
  def canEdit(self):
    """Spradza prawo do edycji - dla dodania nowej wiadomości nie podawać argumentu, 
    dla edycji wpisu dodać mail autora oryginalnego postu"""
    if self.user.email() == 'mikolajsochacki@gmail.com' or self.user.email() == 'radarodzicow.zkpig26gdansk@gmail.com': #admin może edytować
      return True
    else:
      return False
      
  def deletePost(self):
    self.getPost()
    if self.canEdit():
      self.post.delete()
      
      
  def check_resize(self, img_str):
    """zmienia rozmiar - nie zminia obrazków małych,  skaluje proporcjonalnie"""
    img = images.Image(img_str)
    h = float(img.height)
    w = float(img.width)
    if h <= 520.0 and w <= 350.0:
      return "s" #obrazek za mały do skalowania
    prop = w / h
    if prop >= 1.4857142857142858:
      return 'w' #skaluj szerokość
    else:
      return 'h' #skaluj wysokość
    
