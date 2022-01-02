import praw
import json
import os
import re
import yaml
from utils import *
#===Constants===#

class IndieSunday(PluginBase):
    def __init__(self, reddit):
        self.reddit = reddit
        self.posts = self.getCachedSubmissions()
        self.hub = self.reddit.submission('roprhq')

    def streamSubmissions(self):
        subreddit = self.reddit.subreddit(config["subreddit"])
        for log in subreddit.mod.stream.log():
            if log.action == 'removelink':
                self.removeEntry(log.target_permalink)
            if log.action == 'approvelink':
                self.addEntry(log.target_permalink)

    def addEntry(self, permalink):
        url = 'https://www.reddit.com' + permalink
        submission = self.reddit.submission(url=url)
        if submission.link_flair_text == 'Indie Sunday':
            if submission.id not in self.posts:
                self.posts[submission.id] = {
                    'permalink': submission.permalink,
                    'title': submission.title
                }
                self.saveCachedSubmissions()
                self.updateHub()

    def removeEntry(self, permalink):
        url = 'https://www.reddit.com' + permalink
        submission = self.reddit.submission(url=url)
        if submission.link_flair_text == 'Indie Sunday':
            if submission.id in self.posts:
                del self.posts[submission.id]
                self.saveCachedSubmissions()
                self.updateHub()
    
    def updateHub(self):
        gameList = ''
        for post_id in self.posts:
            hyperlink = '[{}]({})'.format(self.posts[post_id]['title'], self.posts[post_id]['permalink'])
            gameList += '* {}\n'.format(hyperlink)
        body = '{}\n\n{}\n{}'.format(config["templateHeader"], gameList, config["templateFooter"])
        self.hub.edit(body)


if __name__ == "__main__":
    #Intialize 
    loadConfig()
    indieSunday = IndieSunday()
    indieSunday.streamSubmissions()