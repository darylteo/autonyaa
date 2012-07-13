# encoding: utf-8

# imports
import urllib2
import feedparser
import simplejson as json
import re
import os

import sched,time

def main():
  
   def getSettings():
      print("Get Settings")

   def getSubscriptions(filename):
      with open(filename,"r") as f:
         return json.loads(
            f.read()
         )

   def getFeed(url):
      print("Read Feed: " + url)

      return feedparser.parse(url)

   def checkSubscriptions(subscriptions):
      def buildRegex(expression):
         expression = re.sub(r"[\[\]\.]",r'\\\g<0>', expression)
         expression = re.sub(r'{{(.+?)}}',r'(?P<\g<1>>.+?)',expression)
         return expression

      def isSubbed(subs,entry):
         for sub in subs:
            if re.match(sub,entry.title):
               return entry

      for group in subscriptions:
         print("Checking Subs for '" + group["name"] + "'")

         titles = map(
            buildRegex,
            group["subs"]
         )
         print(titles) 
         feed = getFeed(group["url"]) 

         matches = [
            entry for entry in 
            [
               isSubbed(titles,entry) for entry in feed.entries 
            ]
            if entry != None
         ]

         downloadFiles(matches)

   def downloadFiles(entries):
      print("Download Files")

      for entry in entries:
         print entry.title,entry.link

   checkSubscriptions(
      getSubscriptions(
         "subscriptions.json"
      )
   )

main()
