import praw
import os

from utils import PluginBase
from plugins import *

class RedditAssitant(PluginBase):
    def __init__(self):
        self.name = "__base"
        self.CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.yaml")
        self.CACHE_DIR = os.path.join(os.path.dirname(__file__), "__cache")
        self.config = self.load_config()
        self.reddit = self.init_reddit()
        self.subreddit = self.reddit.subreddit(self.config["subreddit"])
        self.plugins = self.load_plugins()
        self.cache = self.init_cache()

    def init_reddit(self):
        client = self.config["client"]
        reddit = praw.Reddit(**client)
        return reddit
    
    def init_cache(self):
        if not os.path.isdir(self.CACHE_DIR):
             os.mkdir(self.CACHE_DIR)
        self.load_cache()

    def load_plugins(self):
        plugins = []
        for plugin in self.config["plugins"]:
            plugins.append(globals()[plugin](self.reddit, self.subreddit))
        return plugins

    def stream_subreddit(self):
        comment_stream = self.subreddit.stream.comments(skip_existing=True, pause_after=-1)
        submission_stream = self.subreddit.stream.submissions(skip_existing=True, pause_after=-1)
        mod_stream = self.subreddit.mod.stream.log(skip_existing=True, pause_after=-1)
        while True:
            for comment in comment_stream:
                if comment is None:
                    break
                self.process_comment(comment)
            for submission in submission_stream:
                if submission is None:
                    break
                self.process_submission(submission)
            for mod_log in mod_stream:
                if mod_log is None:
                    break
                self.process_mod_log(mod_log)

    def process_comment(self, comment):
        for plugin in self.plugins:
            plugin.consume_comment(comment)

    def process_submission(self, submission):
        for plugin in self.plugins:
            plugin.consume_submission(submission)
    
    def process_mod_log(self, mod_log):
        for plugin in self.plugins:
            plugin.consume_mod_log(mod_log)

if __name__ == "__main__":
    #Intialize
    assistant = RedditAssitant()
    assistant.stream_subreddit()