import yaml
import os
import logging


class PluginBase:
    def __init__(
        self, name="PluginBase", reddit=None, subreddit=None, config_path=None
    ):
        self.name = name
        self.reddit = reddit
        self.subreddit = subreddit
        self.config_path = config_path
        self._config = None
        logging.info(f"Initialized {self.name}")

    @property
    def config(self):
        if not self._config:
            self._config = self.load_config()
        return self._config

    def load_config(self):
        try:
            logging.debug(f"Loading config file from: {self.config_path}")
            return yaml.load(open(self.config_path).read(), Loader=yaml.FullLoader)
        except Exception as e:
            print(e)
            logging.error(
                "'config.yaml' could not be located. Please ensure 'config.example' has been renamed"
            )
            exit()

    def consume_comment(self, comment):
        pass

    def consume_submission(self, submission):
        pass

    def consume_mod_log(self, mod_log):
        pass

    def consume_modmail(self, modmail):
        pass

    def consume_report(self, mod_log):
        pass


def get_permalink(r_string):
    # Given a partial permalink or object id, return a shortened reddit permalink
    if not r_string:
        return None
    if r_string.startswith("/r/"):
        r_string = r_string.split("/")[4]
    return f"https://redd.it/{r_string}"


def get_user_as_string(reddit_object):
    # Take a reddit object and return its author's name if it has one
    if reddit_object.author:
        return reddit_object.author.name
    else:
        return "[Unable to find user]"


def has_stickied_comment(submission, moderator_name=None):
    # Check for any stickied moderator comments
    # Optionally checks if provided mod name matches
    try:
        comment = submission.comments[0]
        if moderator_name:
            if comment.distinguished and comment.author.name == moderator_name:
                return True
            return False
        else:
            if comment.distinguished:
                return True
            return False
    except IndexError:
        return False
