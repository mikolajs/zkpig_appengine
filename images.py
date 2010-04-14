# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext import db

import database


class Images(webapp.RequestHandler):
   """Podaje obrazki na podstawie key"""
   def get(self):
     imgId = self.request.get("img_id")
     if imgId:
       photo1 = database.Post.get(imgId)
       self.answer(photo1)
     else:  
       imgId = self.request.get("img_idP")
       photo2 = database.ParentsPost.get(imgId)
       self.answer(photo2)
       
   def answer(self, photo):
     nr = self.request.get("nr")
     if nr == '0':
       if photo.img0:
         self.response.headers['Content-Type'] = "image/jpeg"
         self.response.out.write(photo.img0)
       else:
         self.response.out.write("No image")
     elif nr == '1':
       if photo.img1:
         self.response.headers['Content-Type'] = "image/jpeg"
         self.response.out.write(photo.img1)
       else:
         self.response.out.write("No image")
     elif nr == '2':
       if photo.img2:
         self.response.headers['Content-Type'] = "image/jpeg"
         self.response.out.write(photo.img2)
       else:
         self.response.out.write("No image")
     elif nr == '3':
       if photo.img3:
         self.response.headers['Content-Type'] = "image/jpeg"
         self.response.out.write(photo.img3)
       else:
         self.response.out.write("No image")
     else:
       self.response.out.write("No image")
       
       
