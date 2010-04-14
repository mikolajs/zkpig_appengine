# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import db

import os.path

import database
import datetime

class AdminHandler(webapp.RequestHandler):
  
  def __init__(self):
    self.getAuthors()
    
  def get(self):
    #odrzucam wejście innych
    if not self.checkAdmin():
      self.response.out.write('<html><body><head><meta http-equiv="content-type" content="text/html; charset=utf-8" /></head><h1> Nie masz uprawnień administratora <br/><a href="/news"> Powrót </a> </h1><body/><html/>')
      return
    path, subPath = os.path.split(self.request.uri)
    if subPath == 'editor':
      #wywołanie z /admin podstrony editor
      self.make_editorView() #dodawanie edytorów
    elif subPath == 'department':
      #wywołanie z /admin podstrony department
      self.make_departmentView() #dodawanie działów 
    elif subPath == "admin":
      #wywołanie stony głównej panelu admina
      path = os.path.join(os.path.dirname(__file__), 'templates/ADMIN.HTML')
      admin = file(path,"r").read()
      self.response.out.write(admin)
    else:
      rootPath, beforePath = os.path.split(path)
      if beforePath == 'del_department':
        key = db.Key(subPath)
        depDB = database.Department.gql("WHERE __key__ = :1", key)
        depList = depDB.fetch(1)
        if len(depList) > 0:
          depList[0].delete()
        self.redirect(os.path.join(rootPath + '/department'))
      elif beforePath == 'del_editor':
        key = db.Key(subPath)
        authDB = database.Authors.gql("WHERE __key__ = :1", key)
        authList = authDB.fetch(1)
        if len(authList) > 0:
          authList[0].delete()
        self.redirect(os.path.join(rootPath + '/editor')) #!!! bardzo dziwne backslash w orginalnej wersji nie jest potrzebny!!!
      else:
        self.response.out.write('<html><body><head><meta http-equiv="content-type" content="text/html; charset=utf-8" /></head><h1> Błędny link <br/><a href="/admin"> Powrót do panelu Administracyjnego </a> </h1><body/><html/>')
      
      

  def post(self):
    subPath = os.path.split(self.request.uri)[-1]
    if subPath == 'department':
      depart = self.request.get('name')
      fullname = self.request.get('fullname')
      if depart.strip() != '' and fullname.strip() != '':
        department = database.Department()
        department.department = depart
        department.name = fullname
        department.put()
      self.make_departmentView()
    elif subPath == 'editor':
      name = self.request.get('name')
      mail = self.request.get('email')
      if name.strip() != '' and mail.strip() != '': 
        author = database.Authors()
        author.name = name
        author.email = mail
        author.put()
      self.make_editorView()
    
  
  def show_content(self):
    """Wysyła formatkę do edycji lub informację o niemożliwości edycji 
       bez zalogowania""" 
    if self.checkAdmin():
      path = os.path.join(os.path.dirname(__file__), 'templates/ADMIN.HTML')
      self.response.out.write(template.render(path, self.page_content)) 
    else:
      self.response.out.write('<html><body><head><meta http-equiv="content-type" content="text/html; charset=utf-8" /></head><h1> Niestety nie masz uprawnień do zarządania stroną. Najpierw zaloguj się! <br/><a href="/news"> Powrót </a> </h1><body/><html/>'  )
        
  def getAuthors(self):
    auth = database.Authors.all()
    self.page_content = {'authors':auth }
    
  def getDepartment(self):
    dep = database.Department.all()
    self.page_content = { 'deps': dep }
  
  def validateAuthor(self):
    pass
  
  def checkAdmin(self):
    currentUser = users.get_current_user()
    #przeniesienie na stronę logowania google
    if not currentUser:
      #self.redirect(users.create_login_url(self.request.uri))
      return False
      #stąd wyrzuca ze skryptu i wywołuje od nowa (chyba)
    if currentUser.email() == "mikolajsochacki@gmail.com":
      return True
    else:
      return False
      
  def make_departmentView(self):
    """tworzymy widok dla dodawania działów"""
    #zrobić wypełnienie page_content
    self.getDepartment()
    path = os.path.join(os.path.dirname(__file__), 'templates/ADMIN_D.HTML')
    self.response.out.write(template.render(path, self.page_content))
  
  def make_editorView(self):
    """tworzę widok dla dodawania użytkowników"""
    #zrobić wypełnienie page_content
    self.getAuthors()
    path = os.path.join(os.path.dirname(__file__), 'templates/ADMIN_U.HTML')
    self.response.out.write(template.render(path, self.page_content))
  
