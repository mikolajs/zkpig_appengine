# -*- coding: utf-8 -*-


from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import db

import os.path
import validator

import database
import datetime

class TestingHandler(webapp.RequestHandler):
     
  def get(self):
    self.findKey()

  def post(self):
    self.show_alterContent()
  
  def show_alterContent(self):
    text = """ oto jest jakiś tekst
    może nie za ciekawy ale ma [b] tagi [/b]
    [color=red] może działają [/color] """
    content = validator.validatePost(text)
    self.response.out.write('<html><body><head><meta http-equiv="content-type" content="text/html; charset=utf-8" /></head><h1>Test:</h1> %s <br/> <body/><html/>'% (content))
  
  def show_content(self):
    dep = database.Department.gql("WHERE department = :1",'Sport')
    depart = dep.fetch(1)
    postsTem = database.Post.gql("WHERE department = :1", depart[0])
    posts = postsTem.fetch(20)
    content = ""
    for post in posts:
      key = post.key()
      content = 'author: %s, body: %s, title %s, edit_dateStr: %s, department %s skrot %s <br/> key: %s' % (post.author.name,post.body,post.title, post.creation_dateStr, post.department.department, post.department.name, key.id() )
    #content = 'pelna nazwa: %s, skrot: %s' % (depart[0].name, depart[0].department)
    self.response.out.write('<html><body><head><meta http-equiv="content-type" content="text/html; charset=utf-8" /></head><h1>Test:</h1> %s <br/> <body/><html/>'% (content))
    
  def findKey(self):
    postsTem2 = database.Post.all()
    posts2 = postsTem2[0]
    k = posts2.key()
    if k:
      postsTem = database.Post.gql("WHERE __key__ = :1", k)
      posts = postsTem.fetch(1)
    content = ""
    for post in posts:
       content = 'author: %s, body: %s, title %s, edit_dateStr: %s, department %s skrot %s <br/> key: %s' % (post.author.name,post.body,post.title, post.creation_dateStr, post.department.department, post.department.name, post.key().id() )
    self.response.out.write('<html><body><head><meta http-equiv="content-type" content="text/html; charset=utf-8" /></head><h1>Test:</h1> %s <br/> <body/><html/>'% (content))
       
       