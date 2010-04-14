#!/usr/bin/env python

import gdata.photos.service
import gdata.media
import gdata.geo

import os.path


class GalleryCron():
  
    
  def __client(self):
    self.galleryStr = ""
    self.imageUrls = '[ '
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
      self.imageUrls += urlsArr
      self.galleries.append(gal)
    self.imageUrls += ' ]'
      
  def insertInDB(self):
    """metoda uruchamiająca pobranie danych i zapis do bazy danych"""
    self.__client()







var gallerieArr =  [{% for i in galleries %} [{{i.id_nr}},  {{i.pictures_numb}}, '{{i.path}}', '{{i.title}}', '{{i.description}}' ] , {% endfor %}]
  
  var urlsArr = [ {%for j in urlsArr %} {{j}} , {%endfor%} ]
