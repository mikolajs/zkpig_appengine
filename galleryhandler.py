# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import gdata.photos.service
import gdata.media
import gdata.geo

import os.path


class Gallery():
  nr = '' #nr galerii po kolei
  id_nr = '' #nr id googla galerii
  pictures_numb = '' #ilość zdjęć w galeri
  path = 'http://fullpath.png'
  title = 'title'
  description = 'Empty'
  

#################################################################
#webapp.RequestHandler
class GalleryHandler(webapp.RequestHandler):
  
  def get(self):
    self.answer()
  
  def post(self):
    self.answer()
  
  def answer(self):
    #content = template.render('templates/GALLERY_CONTENT.HTML',galleries)
    self.client()
    self.page_content = {'galleryLen':len(self.galleries),'galleries':self.galleries, 'urlsArr':self.urlsArr}
    self.response.out.write(template.render('templates/GALLERY.HTML', self.page_content))
    
  def client(self):
    self.galleries = []
    gd_client = gdata.photos.service.PhotosService()
    gd_client.email = "zkpig26gdansk@gmail.com"
    gd_client.password = "lgOS1971as"
    gd_client.source = 'exampleCo-exampleApp-1'
    gd_client.ProgrammaticLogin()
    albums = gd_client.GetUserFeed().entry 
    self.urlsArr = []
    index = 0
    for album in albums:
      gal = Gallery()
      gal.nr = str(index)
      index += 1
      gal.id_nr = album.gphoto_id.text
      gal.pictures_numb = album.numphotos.text
      gal.title = album.title.text
      gal.description = album.summary.text
      gal.path = album.media.thumbnail[0].url
      photos = gd_client.GetFeed('/data/feed/api/user/default/albumid/%s?kind=photo' % (album.gphoto_id.text))
      urlsString = " [ "
      for photo in photos.entry:
        urlsString += "['"
        urlsString +=  photo.media.thumbnail[1].url
        urlsString += "','"
        urlsString += photo.content.src
        urlsString += "'] , "
      urlsString = urlsString[:-2] + " ]"
      self.urlsArr.append(urlsString)
      self.galleries.append(gal)
      
      
 