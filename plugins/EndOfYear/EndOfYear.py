import praw
import json
import os
import re
import yaml

#===Constants===#
CONFIG_FILE = os.path.join(os.path.dirname(__file__),"config.yaml")
CACHE_FILE =  os.path.join(os.path.dirname(__file__), "cache.json")

#===Globals===#
#Config file
config = None

def loadConfig():
    global config
    #Load configs
    try:
        config = yaml.load(open(CONFIG_FILE).read(), Loader=yaml.FullLoader)
    except:
        print("'config.yaml' could not be located. Please ensure 'config.example' has been renamed")
        exit()

class EndBot:
    def __init__(self):
        self.reddit = self.initReddit()
        self.cache = self.getCachedSubmissions()
        self.posts = [
            "rg9are",
            "rgd2j9",
            "rh104v",
            "rhrbm8",
            "rii1l0",
            "rja2b9",
            "rkpivo",
            "rlfa3l",
            "rm660l",
            "rmxw8s",
            "rnpana",
            "robcwv",
            "rpq28f",
            "rqi1gu",
            "rr9k3f"
        ]
        for post in self.posts:
            if post not in self.cache:
                self.cache[post] = {}

    def getCachedSubmissions(self):
        cache = {}
        try:
            with open(CACHE_FILE, "r") as fin:
                cache = json.load(fin)
        except Exception as e:
            print (e)
        return cache
    
    def saveCachedSubmissions(self):
        with open(CACHE_FILE, "w") as fout:
            for chunk in json.JSONEncoder().iterencode(self.cache):
                fout.write(chunk)

    def initReddit(self):
        client = config["client"]
        reddit = praw.Reddit(**client)
        return reddit

    def streamComments(self):
        subreddit = self.reddit.subreddit("games")
        for comment in subreddit.stream.comments(skip_existing=True):
            parent_id = comment.link_id.split('_')[1]
            if parent_id in self.posts and 't3_' in comment.parent_id:
                print(comment.body)
                try:
                    nomination = comment.body.split('**')[1].lower()
                    nomination = re.sub(r'\W+', '', nomination)
                    print(nomination)
                    if nomination not in self.cache[parent_id]:
                        self.addNomination(nomination, comment)
                    else:
                        print("DUPLICATE! {}".format(nomination))
                        nomination_link = self.cache[parent_id][nomination]
                        self.removeComment(comment, nomination_link)
                except:
                    print("No bold found")

    
    def addNomination(self, nomination, comment):
        parent = comment.link_id.split('_')[1]
        self.cache[parent][nomination] = comment.permalink
        print("Added: {}".format(nomination))
        self.saveCachedSubmissions()

    def removeComment(self, comment, nomination_link):
        comment.mod.remove(mod_note="Duplicate EOY nomination (Automated removal)")
        message = '''Your nomination was removed because there is an existing 
                    nomination for this located here:\n\n{}\n\nThis message was sent by a bot,
                    please reply if you believe this removal was a mistake'''.format(nomination_link)
        comment.mod.send_removal_message(message=message,
                                        title="Duplicate Nomination",
                                        type="private")
if __name__ == "__main__":
    #Intialize 
    loadConfig()
    endbot = EndBot()
    endbot.streamComments()