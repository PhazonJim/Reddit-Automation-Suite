import praw
import os
import sys
sys.path.append('.')
import utils
from plugins import *

class RedditAssitant:
    def __init__(self):
        CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.yaml")
        self.config = utils.loadConfig(CONFIG_FILE)
        self.reddit = self.initReddit()
        self.plugins = self.loadPlugins()

    def initReddit(self):
        client = self.config["client"]
        reddit = praw.Reddit(**client)
        return reddit

    def loadPlugins(self):
        plugins = []
        for plugin in self.config["plugins"]:
            plugins.append(globals()[plugin](self.reddit))
        return plugins

    def streamSubreddit(self):
        subreddit = self.reddit.subreddit(self.config["subreddit"])
        comment_stream = subreddit.stream.comments(skip_existing=True, pause_after=-1)
        submission_stream = subreddit.stream.submissions(skip_existing=True, pause_after=-1)
        mod_stream = subreddit.mod.stream.log(skip_existing=True, pause_after=-1)
        while True:
            for comment in comment_stream:
                if comment is None:
                    break
                self.processComment(comment)
            for submission in submission_stream:
                if submission is None:
                    break
                self.processSubmission(submission)
            for modlog in mod_stream:
                if modlog is None:
                    break
                self.processModLog(modlog)

    def processComment(self, comment):
        for plugin in self.plugins:
            plugin.consumeComment(comment)

    def processSubmission(self, submission):
        for plugin in self.plugins:
            plugin.consumeSubmission(submission)
    
    def processModLog(self, modlog):
        for plugin in self.plugins:
            plugin.consumeModLog(submission)

if __name__ == "__main__":
    #Intialize
    assistant = RedditAssitant()
    assistant.streamSubreddit()