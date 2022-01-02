import praw
import os
import sys

sys.path.append('.')
import utils
from plugins import *

class RedditAssitant:
    def __init__(self):
        CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.yaml")
        self.config = utils.load_config(CONFIG_FILE)
        self.reddit = self.init_reddit()
        self.plugins = self.load_plugins()

    def init_reddit(self):
        client = self.config["client"]
        reddit = praw.Reddit(**client)
        return reddit

    def load_plugins(self):
        plugins = []
        for plugin in self.config["plugins"]:
            plugins.append(globals()[plugin](self.reddit))
        return plugins

    def stream_subreddit(self):
        subreddit = self.reddit.subreddit(self.config["subreddit"])
        comment_stream = subreddit.stream.comments(skip_existing=True, pause_after=-1)
        submission_stream = subreddit.stream.submissions(skip_existing=True, pause_after=-1)
        mod_stream = subreddit.mod.stream.log(skip_existing=True, pause_after=-1)
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
                if modlog is None:
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