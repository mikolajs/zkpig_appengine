#!/usr/bin/python2.5
# -*- coding: utf-8 -*-
# Licensed under the GPL, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.

# AppEngine
from google.appengine.ext import db

# Python
import datetime
import logging
import validator

# Maximun allowable string length for title?
_MAX_STRING_LENGTH = 500

# Maximum allowable link length
_MAX_LINK_LENGTH = 2083


def ValidateStringLenth(value, max_length=_MAX_STRING_LENGTH):
  """Checks if the given string is too long.

  Args:
    value: user input to be checked
    max_length: int corresponding to the maximum length of the given |value|

  Returns:
    Boolean: True if acceptable, False if too long.
  """
  if isinstance(value, basestring):
    if len(value) <= max_length:
      return True
  return False

class Department(db.Model):
  """Department entity"""
  department = db.StringProperty(multiline=False) #skrótowa nazwa na pasek
  name = db.StringProperty(multiline=False) # pełna nazwa

class Authors(db.Model):
  """User entity."""
  name = db.StringProperty(multiline=False) # full name
  email = db.StringProperty(multiline=False) # gmail
  #login = db.StringProperty() # login
  #password = db.StringProperty() # haslo
  #privilages = db.StringProperty() #dostęp do zapisu w działach


class Post(db.Model):
  """Post entity."""
  author = db.ReferenceProperty(Authors)
  body = db.TextProperty()
  title = db.StringProperty(multiline=False) #max=500
  #comment_count = db.IntegerProperty(default=0)
  #is_published = db.BooleanProperty(default=False)
  edit_dateStr = db.StringProperty()
  creation_date = db.DateTimeProperty()
  creation_dateStr = db.StringProperty()
  # Meta info for this post
  img0 = db.BlobProperty() #obrazek tytułowy
  img1 = db.BlobProperty() 
  img2 = db.BlobProperty() 
  img3 = db.BlobProperty() 
  department = db.ReferenceProperty(Department)


class Parents(db.Model):
  """Parents allowed to insert posts"""
  name = db.StringProperty()
  email = db.StringProperty()

class ParentsPost(db.Model):
  """Parents can post in other page"""
  #author = db.ReferenceProperty(Parents)
  body = db.TextProperty()
  title = db.StringProperty()
  img0 = db.BlobProperty() #obrazek tytułowy
  img1 = db.BlobProperty() 
  img2 = db.BlobProperty() 
  img3 = db.BlobProperty() 
  creation_date = db.DateTimeProperty()
  creation_dateStr = db.StringProperty()
