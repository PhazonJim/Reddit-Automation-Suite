import re
import os
import yaml
from ...utils import PluginBase, get_full_permalink, get_user_as_string


class RemovalReasons(PluginBase):
    def __init__(self, reddit, subreddit):
        PluginBase.__init__(
            self,
            name="RemovalReasons",
            reddit=reddit,
            subreddit=subreddit,
            config_path=os.path.join(os.path.dirname(__file__), "config.yaml"),
        )

    def consume_mod_log(self, mod_log):
        self.check_removals(mod_log)

    def check_removals(self, mod_log):
        permalink = get_full_permalink(mod_log.target_permalink)
        if (
            mod_log.action == "removelink"
            and mod_log._mod not in self.config["ignored_moderators"]
        ):
            submission = self.reddit.submission(url=permalink)
            rule = self.get_rule_from_regex_match(submission.link_flair_text)
            self.submit_comment(submission, rule)

    def get_rule_from_regex_match(self, flair):
        regexes = self.config["regexes"]
        if not flair:
            return None
        flair = flair.strip().replace(" ", "").lower()
        for rule in regexes:
            if re.search(regexes[rule], flair):
                return rule
        return None

    def submit_comment(submission, submissionRule, removalReasons):
        user = get_user_as_string(submission)
        commentBody = f"Hello /u/{user},\n\n"
        commentBody += removalReasons["header"]
        commentBody += removalReasons["rules"][submissionRule]
        commentBody += removalReasons["footer"]
        comment = submission.reply(commentBody)
        comment.mod.distinguish(how="yes", sticky=True)
        comment.mod.lock()
        return comment

    def getRemovalReasons(self, reddit):
        # Grab the removal reasons from the wiki
        wikiPage = (
            self.subreddit(self.config["wiki_subreddit"])
            .wiki[self.config["removal_reasons_wiki"]]
            .content_md
        )
        return yaml.load(wikiPage, Loader=yaml.FullLoader)

    def checkForDuplicateComments(submissionObj):
        # Check top level comments in the submission object
        submissionObj.comments.replace_more(limit=0)
        return any(comment.distinguished for comment in submissionObj.comments)
