# -*- coding: utf-8 -*-

#import database
import re
#import database


class Validator:
  """Zamienia teksty wprowadzone do formatki w tagi 
     usuwa tagi html (oprócz <b>,<i>,<u>, <img src="img\?img_id=.*?"/>  wprowadzone przez użytkownika"""
  def __init__(self):
    self.__Tags = ('<b>','</b>','<i>','</i>','<u>','</u>') #dozwolone tagi + img
    self.string = ""

  def validatePost(self, post):
    """główna metoda robiąca porządek przed wstawieniem do bazy"""
    post.title = self.validateTitle(post.title)
    post.body = self.validateBody(post.body)
    
  def loadPost(self, post):
    """główna metoda ładująca post"""
    self.string = post.body
    self.__loadPost() # wykonuje cała pracę
    post.body = self.string

  def validateTitle(self, string):
    self.string = string
    self.eraseTags()
    return self.string
    
  def validateBody(self, string):
    """zamienia return na </br>,usuwa niedozwolone tagi, 
    (w przyszłości) sprawdza poprawność tagów (zamknięcia), wymiana [img] na <img> na  """
    self.string = string  
    self.eraseTags()
    self.__BBCtoHTML()
    #tu zrobić sprawdzenie parzystości tagów
    postList =  self.string.split('\n')
    string = ""
    for i in postList:
      string += i.strip()
      string += '<br/>'
    return string
    
  def __loadPost(self):
    """zamienia wszystkie tagi html na bbcode przed załadowaniem posta do edycji"""
    #tag_imgBegin =  '<img src="img?img_id=%s' % (self.id_key)
    #self.string = self.string.replace(tag_imgBegin + '&nr=0" />',' ')
    #self.string = self.string.replace(tag_imgBegin + '&nr=1" />','[img1]')
    #self.string = self.string.replace(tag_imgBegin + '&nr=2" />','[img2]')
    #self.string = self.string.replace(tag_imgBegin + '&nr=3" />','[img3]')
    #Zamienia tagi HTML na BBCode przy ładowaniu!!!
    bbCodeOpen = ['<b>' ,'<i>', '<u>' ]
    bbCodeClose = ['</b>', '</i>', '</u>' ]
    for i in bbCodeOpen:
      self.string = self.string.replace(i, '[' + i[1] +  ']')
    for i in bbCodeClose:
      self.string = self.string.replace(i, '[/' + i[2] +  ']')
    self.string = self.string.replace('<br/>','\n')
    self.__remakeLink()

  def eraseTags(self):
    """Usuwanie niedozwolonych tagów """
    tagRe = re.compile('(<.*>)')
    tagToErase = tagRe.search(self.string)
    while tagToErase:
      self.string = self.string.replace(tagToErase.group(0),"")
      tagToErase = tagRe.search(self.string)
      
    
  def __isTagToErase(self, tag):
    """sprawdza czy tag ma być usunięty"""
    for t in self.__Tags:
      if tag == t:
        return False
    return True
      
  def __BBCtoHTML(self,):
    """Sprawdza poprawność tagów """
    self.bbc_tag = [('[b]','[/b]','<b>','</b>'),('[i]','[/i]','<i>','</i>'),('[u]','[/u]','<u>','</u>')]
    self.__stackChecker()
    self.__makeLink()
    
        
  #def __checkBBC(self,i1,i2):
    #for bbcT in self.bbc_tag:
      #i1 = 0
      #i2 = 0
      #while i1 != -1 and i2 != -1 and i2 < len(self.string):
        #i1 = self.string.find(bbcT[0],i1)
        #i2 = self.string.find(bbcT[1],i1)
        #print i1, i2
        #if i1 != -1 and i2 != -1:
          #self.__checkBBC(i1 + 3, i2 - 4)
          #self.string = self.string[0:i1] + bbcT[2] + self.string[i1+3:]
          #self.string = self.string[0:i2] + bbcT[3] + self.string[i2+4:]
        #if i1 != -1 or i2 != -1:
          #if i1 != -1:
            #self.string = self.string[0:i1] + self.string[i1+3:]
          #if i2 != -1:
            #self.string = self.string[0:i2] + self.string[i2+3:]
        #i1  = i2
    
  #def __getDataBBC(self):
    #self.listBBC = []
    #self.listIndex = []
    #i = 0
    #while i < len(self.string) - 3:
      #if self.string[i] == '[':
        #if (self.string[i+1] == 'b' or self.string[i+1] == 'u' or self.string[i+1] == 'i') and self.string[i+2] == ']':
          #self.listBBC.append(self.string[i+1].upper())
          #self.listIndex.append(i)
        #if self.string[i+1] == '/' and (self.string[i+2] == 'b' or self.string[i+2] == 'u' or self.string[i+2] == 'i') and self.string[i+3] == ']':
          #self.listBBC.append(self.string[i+2])
          #self.listIndex.append(i)
      #i += 1
      
  def __stackChecker(self):
    #sprawdza poprawność bbc i zamienia mające parę kody na html
    self.stackBBC = ''
    self.indexList = []
    i = 0
    while i < len(self.string) - 3:
      if self.string[i] == '[':
        if (self.string[i+1] == 'b' or self.string[i+1] == 'u' or self.string[i+1] == 'i') and self.string[i+2] == ']':
          self.stackBBC = self.stackBBC + self.string[i+1]
          self.indexList.append(i)
        if self.string[i+1] == '/' and (self.string[i+2] == 'b' or self.string[i+2] == 'u' or self.string[i+2] == 'i') and self.string[i+3] == ']':
          #jeżeli się zgadza usuwam ze stosu i zamieniam bbcode na html
          if len(self.stackBBC) > 0:
            if self.stackBBC[-1] == self.string[i+2]:
              if len(self.indexList) > 0:
                self.string = self.string[0:self.indexList[-1]] + '<' + self.string[i+2] + '>' + self.string[self.indexList[-1]+3:]
                self.string = self.string[0:i] + '</' + self.string[i+2] + '>' + self.string[i+4:]
                self.stackBBC = self.stackBBC[:-1]
                self.indexList = self.indexList[:-1]
      i += 1
  
  
  def __makeLink(self):
    #szukanie bbc linków i zamiana na html
    reLink = re.compile('\[l=(.*?)\](.*?)\[/l\]')
    toChange = reLink.search(self.string)
    security = 5
    while toChange:
      if security < 0:
        break
      else:
        whatChangeStr = '[l=' + toChange.group(1) + ']' + toChange.group(2) + '[/l]'
        howChangeStr = '<a href="' + toChange.group(1) + '" target="_blank">' + toChange.group(2) + '</a>'
        self.string = self.string.replace(whatChangeStr,howChangeStr)
        toChange = reLink.search(self.string)
        security -= 1
      
  def __remakeLink(self):
    #przywraca bbc linki z html przy ładowaniu do edytora
    reLink = re.compile('<a href="(.*?)" target="_blank">(.*?)</a>')
    toChange = reLink.search(self.string)
    security = 5
    while toChange:
      if security < 0:
        break
      else:
        whatChangeStr = '<a href="' + toChange.group(1) + '" target="_blank">' + toChange.group(2) + '</a>'
        howChangeStr = '[l=' + toChange.group(1) + ']' + toChange.group(2) + '[/l]'
        print whatChangeStr
        self.string = self.string.replace(whatChangeStr,howChangeStr)
        toChange = reLink.search(self.string)
        security -= 1
  
  def forTest(self,string):
    self.string = string
    print "HTML"
    self.__makeLink()
    print self.string
    print "BBCode"
    self.__remakeLink()
    print self.string
    
    

if __name__ == "__main__":
  f = file('templates/NEWS.HTML','r')
  t = f.read()
  val = Validator()
  #val.forTest(t)
  t = """Jakiś  ciekawy  ciekawy zapis  informacji na jakiś temat
skdjf i ksdjf ids ksdjf ids dkfj ods kdjf
ksdfj skd [l=http://wp.pl/sdkokdjfodkjfdkjfkdjskdjfsdjfsdjksjdkjdfjsdjksdjksdjkjfskjdksjdfsjdkjdjfsodfjsdkjfsdjo] lskdjflksdjkjkfj [/l] lskdjflksdjkjkfj  jdhf sjdh djhd  [l=http://up.pl/sdkddfdfdfdfa=df&%#$)(*&^#kjfkdjskdjfsdjfsdjksjdkjdfjkjdksjdfsjdkjdjfsodfjsdkjfsdjo] lskdjflksdjkjkfj [/l] kjkdsjfkdsjf"""
  val.forTest(t)
  
