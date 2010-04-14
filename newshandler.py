# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users

import os.path

import database

class NewsHandler(webapp.RequestHandler):
  """Wyświetla wiadomości"""
  def get(self):
    self.getId()
    self.answer()

  def post(self):
    self.getId()
    self.answer()
  
  def answer(self):
    self.response.out.write(template.render('templates/NEWS.HTML', self.page_content))
  
  def __init__(self):
    self.createDefalutContent()
      
  def createDefalutContent(self):
    
    username = 'anonimowy'
    loginfo = 'zaloguj'
    departments = database.Department.all()
    user = users.get_current_user()
    if user:
      username = user.email()
      loginfo = 'wyloguj'
    
    self.page_content = { 'loginfo':loginfo, 'departmentName':"Ostatnie wpisy", 'username':username, 'departments':departments, 'content':'Brak wiadomości.', 'showcreate':False,'departmentShort':'Nowości' }
    
  def getId(self):
    """pobieram id wybranego działu wpisuje treść skrótów wiadomości z danego działu 
       wywołuje getLatest() gdy chce wpisać ostatnie wiadomości"""
    departmentStr = self.request.get('id')
    if departmentStr == 'last' or departmentStr == "":
      posts = self.getLatest()
      self.page_content['departmentName'] = "Ostatnie wpisy"
      self.page_content['showcreate'] = False
      self.page_content['departmentShort'] = 'Nowości'
    else:
      departRes = database.Department.gql("WHERE department = :1 ",departmentStr) 
      depart = departRes.fetch(1)
      results = database.Post.gql("WHERE department = :1 " + "ORDER BY creation_date DESC",depart[0]) # dopisano ORDER BY creation_date DESC
      posts = results.fetch(20)
      if len(depart) > 0:        
        self.page_content['departmentName'] =  depart[0].name #dodaje opis działu
        self.page_content['showcreate'] = self.isEditor(self.page_content['username'])
        self.page_content['departmentShort'] = depart[0].department
      else: 
        self.page_content['departmentName'] =  "error" #dodaje opis działu
        self.page_content['showcreate'] = False
        self.page_content['departmentShort'] = 'Error'
    for post in posts:
      post.body = post.body[0:300]
      post.body = post.body.replace('[img1]','')
      post.body = post.body.replace('[img2]','')
      post.body = post.body.replace('[img3]','')
      
      post.body = post.body.split("<br/><br/>")[0] #pusta linia separuje wstęp od całego postu
    articles = {'posts':posts} 
    self.page_content['content'] = template.render('templates/CONTENT.HTML',articles)
    
      
  def getLatest(self):
    """pobiera ostatnie wiadomośccdi"""
    results = database.Post.gql("ORDER BY creation_date DESC")
    return results.fetch(20)
      
  def isEditor(self, mail):
    auth = database.Authors.all()
    for a in auth:
      if a.email == mail:
        return True
    return False
