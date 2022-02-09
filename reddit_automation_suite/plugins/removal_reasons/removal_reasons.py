import re
import os
import yaml
import logging
from ...reddit_utils import (
    PluginBase,
    get_permalink,
    get_user_as_string,
    has_stickied_comment,
)


class RemovalReasons(PluginBase):
    def __init__(self, reddit, subreddit):
        PluginBase.__init__(
            self,
            name="RemovalReasons",
            reddit=reddit,
            subreddit=subreddit,
            config_path=os.path.join(os.path.dirname(__file__), "config.yaml"),
        )
        self.removal_reasons = self.get_removal_reasons()
        self.moderator_name = self.reddit.user.me().name

    def consume_mod_log(self, mod_log):
        # If the mod_log action is an edited flair, process the submission
        if mod_log.action == "editflair" and mod_log._mod not in self.config.get(
            "ignored_moderators", []
        ):
            permalink = get_permalink(mod_log.target_permalink)
            submission = self.reddit.submission(url=permalink)
            self.process_submission_flair(submission)

    def process_submission_flair(self, submission):
        # Check to see if the submission flair matches our regexes, if it does add a removal message
        removal_rule = self.get_rule_from_regex_match(submission.link_flair_text)
        if removal_rule:
            if has_stickied_comment(submission, moderator_name=self.moderator_name):
                self.remove_stickied_comment(submission)
            logging.info(
                f"Adding removal message for Rule {removal_rule} at {submission.permalink}"
            )
            comment_body = self.build_removal_comment_body(submission, removal_rule)
            self.submit_comment(submission, comment_body)

    def get_rule_from_regex_match(self, flair):
        # Check submission flair against configured regex patterns to get associated removal rule
        regexes = self.config.get("regexes")
        if not flair:
            return None
        flair = flair.strip().replace(" ", "").lower()
        for rule in regexes:
            if re.search(regexes.get(rule), flair):
                return rule
        return None

    def build_removal_comment_body(self, submission, removal_rule):
        # Build a removal message to leave on the removed submission
        user = get_user_as_string(submission)
        comment_body = f"Hello /u/{user},\n\n"
        comment_body += self.removal_reasons.get("header")
        comment_body += self.removal_reasons.get("rules").get(removal_rule)
        comment_body += self.removal_reasons.get("footer")
        return comment_body

    def submit_comment(self, submission, comment_body):
        # Submit a moderator comment and sticky/lock it
        comment = submission.reply(comment_body)
        comment.mod.distinguish(how="yes", sticky=True)
        comment.mod.lock()

    def get_removal_reasons(self):
        # Grab all removal messages from configurable reddit wiki
        wikiPage = self.subreddit.wiki[
            self.config.get("removal_reasons_wiki")
        ].content_md
        return yaml.load(wikiPage, Loader=yaml.FullLoader)

    def remove_stickied_comment(self, submission):
        # Remove sticked moderator comment
        submission.comments[0].mod.remove()
