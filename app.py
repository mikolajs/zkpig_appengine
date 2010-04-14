#!/usr/bin/python2.4
# -*- coding: utf-8 -*-
#
# Copyright 2009 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Main function that handles passing requests to appropriate handlers."""

# AppEngine
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

# Cruise Control
#from handlers import admin
import schoolhandler
import newshandler
import galleryhandler
import adminhandler
import loginhandler
import testing
import articlehandler
import pieceofnews
import images
import parentshandler
import parentsnewshandler
import parentsarticlehandler


HANDLERS = [('/', schoolhandler.SchoolHandler),
            ('/index/?',  schoolhandler.SchoolHandler),
            ('/index\.html',  schoolhandler.SchoolHandler),
            ('/school/?', schoolhandler.SchoolHandler),
            ('/news/?',newshandler.NewsHandler),
            ('/gallery/?',galleryhandler.GalleryHandler),
            ('/article/?',articlehandler.ArticleHandler),
            ('/pieceofnews/?',pieceofnews.PieceofnewsHandler),
            ('/admin/?.*',adminhandler.AdminHandler),
            ('/login/?',loginhandler.LoginHandler),
            ('/parentsarticle/?',parentsarticlehandler.ArticleHandler),
            ('/parentsnews/?',parentsnewshandler.ParentsNewsHandler),
            ('/parents/?',parentshandler.ParentsHandler),
            ('/img',images.Images),
            ('/testing/?',testing.TestingHandler), #testowe!!!!
            ('/.*',  schoolhandler.SchoolHandler)]
            
def main():
  # NOTE: Set debug to True when pushing to testing changes
  application = webapp.WSGIApplication(HANDLERS, debug=True)
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
