from utils import *

class Foo(PluginBase):
    def __init__(self, reddit, subreddit):
        self.reddit = reddit
        self.subreddit = subreddit
        print("I am alive")
    
    def consume_comment(self, comment):
        print(comment.body)
    
    def consume_submission(self, submission):
        print(submission.permalink)
    
    def consume_mod_log(self, mod_log):
        print(mod_log.target_permalink)