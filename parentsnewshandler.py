# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users

import os.path

import database
import parentsbase


class ParentsNewsHandler(parentsbase.ParentsBase):
  def get(self):
    self.act = self.request.get('id')
    self.nmb = self.request.get('nmb')
    self.showPost()
  
  def post(self):
    #self.answer()
    pass
    
  def answer(self):
    """pokazuje listę postów i umożliwia zalogowanemu administratorowi postów ich dodawanie"""
    pass

  def isLogedParent(self):
    """sprawdza czy jest ktoś zalogowany i czy może dodawać posty"""
    user = users.get_current_user()
    if user:
      mail = user.email()
      if mail == 'radarodzicow.zkpig26gdansk@gmail.com' or mail == 'mikolajsochacki@gmail.com':
        return True
    return False
    
  def showPost(self):
    """pokazuje wybrany post"""
    self.makeMenu() #od rodzica 
    key = db.Key(self.nmb)
    postsTem = database.ParentsPost.gql("WHERE __key__ = :1", key)
    parentPost = postsTem.fetch(1)[0]
    loged = self.isLogedParent()
    tag_imgBegin =  '<img src="img?img_idP=%s' % (parentPost.key())
    parentPost.body = parentPost.body.replace('[img1]',tag_imgBegin + '&nr=1" />')
    parentPost.body = parentPost.body.replace('[img2]',tag_imgBegin + '&nr=2" />')
    parentPost.body = parentPost.body.replace('[img3]',tag_imgBegin + '&nr=3" />')
    self.page_content["parentPost"] = parentPost
    self.page_content['loged'] = loged
    self.response.out.write(template.render('templates/PARENTSNEWS.HTML', self.page_content))
    

