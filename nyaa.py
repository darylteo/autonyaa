# encoding: utf-8

import urllib2
import feedparser
import simplejson as json
import re
import os



def initSettings(url):
   if(not os.path.isfile(url)):
      f = open(url,'w')
      f.write(
         json.dumps({
            "subscriptions_file": "subscriptions.json",
            "target_url": "target",
            "history_file": "history.json"
         })
      )
      f.close()

def initFiles(subs_url,history_url,target_url):
   if(not os.path.isfile(subs_url)):
      f = open(subs_url,'w')
      f.write('[]')
      f.close()

   if(not os.path.isfile(history_url)):
      f = open(history_url,'w')
      f.write('[]')
      f.close()

   if(not os.path.isdir(target_url)):
      os.makedirs(target_url)


def isSubbed(subs,title):
   for sub in subs:
      matches = re.match(sub,title)
      if matches:
         return (True,int(matches.group('episode')))

   return (False,'-1')

def loadSubscriptions(url):
   f = open(url,'r')
   subs = json.loads(
      f.read() 
   )
   f.close()

   return subs

def loadSettings(url):
   f = open(url,'r')
   settings = json.loads(
      f.read()
   )
   f.close()

   return settings

def loadFeed(url):
   return feedparser.parse(url)


def loadHistory(url):
   f = open(url,'r')
   history = json.loads(
      f.read()
   )
   f.close()

   return set(history)

def saveHistory(history,url):
   f = open(url,'w')
   f.write(
      json.dumps(list(history))
   )
   f.close()
  

def downloadToTarget(url,filename,target_url):
   f = urllib2.urlopen(url)
   data = f.read()
   f.close()

   filename = os.path.join(target_url,filename)
   f = open(filename,'w')
   f.write(data)
   f.close()
   

def doUpdateSub(subscription, history):

   def buildRegex(expression):
      expression = re.sub(r"[\[\]\.]",r'\\\g<0>', expression)
      expression = re.sub(r'{{(.+?)}}',r'(?P<\g<1>>.+?)',expression)
      return expression

   data = loadFeed(subscription['feed'])
   subs = subscription['subs']
   subs = map(buildRegex,subs)

   for entry in data.entries:
      subscribed,episode = isSubbed(subs,entry.title)

      if(not subscribed):
         continue

      if(entry.title in history):
         continue

      # download the torrent
      downloadToTarget(
         entry.link + '.torrent',
         entry.title,
         target_url
      )

      # if successful download then add to history
      history.add(entry.title)




def doUpdate():
   initSettings('settings.json')
   settings = loadSettings('settings.json')

   subs_url = settings['subscriptions_file']
   history_url = settings['history_file']
   target_url = settings['target_dir']

   initFiles(
      subs_url,
      history_url,
      target_url
   )

   history = loadHistory(history_url)
   subs = loadSubscriptions(subs_url)

   for sub in subs:
      doUpdateSub(sub,history)

   saveHistory(history,history_url)

def main():
   doUpdate()


main()
   
