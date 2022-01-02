from utils import *

class Foo(PluginBase):
    def __init__(self, reddit):
        self.reddit = reddit
        print("I am alive")
    
    def consumeComment(self, comment):
        print(comment.body)
    
    def consumeSubmission(self, submission):
        print(submission.permalink)
    
    def consumeModLog(self, modlog):
        print(modlog.target_permalink)