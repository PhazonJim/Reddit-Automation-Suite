import os
import re
import utils

class EndBot(utils.PluginBase):
    def __init__(self, reddit, subreddit):
        CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.yaml")
        self.reddit = reddit
        self.subreddt = subreddit
        self.config = utils.load_config(CONFIG_FILE)
        self.cache = utils.load_cache()
        self.posts = []

    def consume_comment(self, comment):
        parent_id = comment.link_id.split("_")[1]
        if parent_id in self.posts and "t3_" in comment.parent_id:
            try:
                nomination = comment.body.split("**")[1].lower()
                nomination = re.sub(r"\W+", "", nomination)
                if nomination not in self.cache[parent_id]:
                    self.addNomination(nomination, comment)
                else:
                    nomination_link = self.cache[parent_id][nomination]
                    self.removeComment(comment, nomination_link)
            except:
                pass # No bold found, handle with Automoderator rule
            
    def consume_submission(self, submission):
        if "/r/Games End of Year" in submission.title:
            if submission.id not in self.posts:
                self.posts.append(submission.id)

    def addNomination(self, nomination, comment):
        parent = comment.link_id.split("_")[1]
        self.cache[parent][nomination] = comment.permalink
        self.saveCachedSubmissions()

    def removeComment(self, comment, nomination_link):
        comment.mod.remove(mod_note="Duplicate EOY nomination (Automated removal)")
        message = '''Your nomination was removed because there is an existing 
                    nomination for this located here:\n\n{}\n\nThis message was sent by a bot,
                    please reply if you believe this removal was a mistake'''.format(nomination_link)
        comment.mod.send_removal_message(message=message,
                                        title="Duplicate Nomination",
                                        type="private")