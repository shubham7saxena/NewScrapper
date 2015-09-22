import webapp2
import sys
import urllib2
import os
import jinja2
import re
import logging
import json
import time

#importing beautifulsoup
sys.path.insert(0, 'libs')
from bs4 import BeautifulSoup

#url to scrap
url = "http://www.wsj.com/"

#setting up jinja2 to pick files from templates dir
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
JINJA_ENVIRONMENT = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

#date and time automatic modifier
localtime = time.asctime( time.localtime(time.time()))

content = urllib2.urlopen(url).read()
soup = BeautifulSoup(content)
tag = soup.findAll('h3')
lis = []
for t in tag:
    temp = []
    tt = t
    h = tt.text
    a = tt.findNext('a')['href']
    l = tt.findNext('span')
    temp.append(h)
    temp.append(a)
    temp.append(l)
    lis.append(temp)

template_values = {
    'dtme': localtime,
    'data': lis,
}

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
