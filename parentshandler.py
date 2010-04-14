# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import mail

import os.path

import database
import parentsbase

class ParentsHandler(parentsbase.ParentsBase):
  
  def get(self):
    self.send = False #info whatever user send post
    self.answer()
  
  def post(self):
    signature = self.request.get('signature')
    name = self.request.get('name')
    content = self.request.get('content')
    if content and content != "":
      self.send = True
      self.insertPostData(content, signature, name)
    else:
      self.send = False
    self.answer()
  
  def answer(self):
    self.makeMenu() # wywołanie metody rodzica
    self.page_content['send'] = self.send
    self.response.out.write(template.render('templates/PARENTS.HTML', self.page_content))
    
  def insertPostData(self, content, signature, posterMail):
    """wysyłanie maila"""
    content += '\nPodpis: ' + signature
    content += '\nE-mail: ' + posterMail
    mail.send_mail("rodzice@zkpig26.appspotmail.com", 'radarodzicow.zkpig26gdansk@gmail.com', 'Wpis ze strony', content)
