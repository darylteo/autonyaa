# encoding: utf-8

# imports
import feedparser
import simplejson as json
import re
import os

import urllib2
import contextlib
import sched,time

def main():
  
   def getSettings(filename):
      with open(filename,"r") as f:
         return json.loads(
            f.read()
         )

   def getSubscriptions(filename):
      with open(filename,"r") as f:
         return json.loads(
            f.read()
         )

   def getNewUpdates(subscriptions):
      def getFeed(url):
         print("Read Feed: " + url)

         return feedparser.parse(url)

      def buildRegex(expression):
         expression = re.sub(r"[\[\]\.]",r'\\\g<0>', expression)
         expression = re.sub(r'{{(.+?)}}',r'(?P<\g<1>>.+?)',expression)
         return expression

      def isSubbed(subs,entry):
         for sub in subs:
            if re.match(sub,entry.title):
               return entry

      matches = []

      for group in subscriptions:
         print("Checking Subs for '" + group["name"] + "'")

         titles = map(
            buildRegex,
            group["subs"]
         )
         print(titles) 
         feed = getFeed(group["url"]) 

         matches.extend([
            (
               entry.title,
               entry.link
            ) for entry in 
            [
               isSubbed(titles,entry) for entry in feed.entries 
            ]
            if entry != None
         ])

      return matches

   def downloadFiles(entries,destination):
      def download(url, target):
         print("Downloading " + url + " to " + target)

         with contextlib.closing(urllib2.urlopen(url)) as r:
            with open(target,"w") as f:
               f.write(r.read()) 


      for title,link in entries:
         download(link,os.path.join(destination,title + ".torrent"))

   settings = getSettings(os.path.join("/usr/lib/autonyaa/settings.json"))

   downloadFiles(
      getNewUpdates(
         getSubscriptions(
            settings["subscription_file"]
         )
      ),
      settings["destination_dir"]
   )

main()
