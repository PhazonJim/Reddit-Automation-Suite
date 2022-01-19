import re
import os
import yaml
import utils

class RemovalReasons(utils.PluginBase):
    def __init__(self, reddit, subreddit):
        CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.yaml")
        self.name = 'RemovalReasons'
        self.reddit = reddit
        self.subreddit = subreddit
        self.config = self.load_config(CONFIG_FILE)
        self.cache = self.load_cache()

def consume_mod_log(self, mod_log):
    self.check_removals(mod_log)

def check_removals(self, mod_log):
    permalink = utils.get_full_permalink(mod_log.target_permalink)
    if mod_log.action == "removelink" and mod_log._mod not in self.config["ignored_moderators"]:
        submission = self.reddit.submission(url=permalink)
        rule = get_rule_from_regex_match(submission.link_flair_text)
        self.submit_comment(submission, rule)

def get_rule_from_regex_match(self, flair):
    regexes = self.config["regexes"]
    if not flair:
        return None
    flair = flair.strip().replace(" ", "").lower()
    for rule in regexes:
        if (re.search(regexes[rule], flair)):
            return rule
    return None

def submit_comment(submission, submissionRule, removalReasons):
    user = utils.get_user_as_string(submission)
    commentBody = f"Hello /u/{user},\n\n"
    commentBody += removalReasons["header"]
    commentBody += removalReasons["rules"][submissionRule]
    commentBody += removalReasons["footer"]
    comment = submission.reply(commentBody)
    comment.mod.distinguish(how="yes",sticky=True)
    comment.mod.lock()
    return comment

def getRemovalReasons(reddit):
    #Grab the removal reasons from the wiki
    wikiPage = reddit.subreddit(config["wiki_subreddit"]).wiki[config["removal_reasons_wiki"]].content_md
    return yaml.load(wikiPage, Loader=yaml.FullLoader)

def checkForDuplicateComments(submissionObj):
    #Check top level comments in the submission object
    submissionObj.comments.replace_more(limit=0)
    return any(comment.distinguished for comment in submissionObj.comments)


