import os
import logging
from importlib import import_module
import praw
from .reddit_utils import PluginBase


class RedditAssitant(PluginBase):
    def __init__(self):
        PluginBase.__init__(
            self,
            name="__base",
            config_path=os.path.join(os.path.dirname(__file__), "config.yaml"),
        )
        self.reddit = self.init_reddit()
        self.subreddit = self.reddit.subreddit(self.config.get("subreddit"))
        self.plugins = self.load_plugins()

    def init_reddit(self):
        client = self.config.get("client", None)
        reddit = praw.Reddit(**client)
        return reddit

    def load_plugins(self):
        plugins = []
        for plugin in self.config.get("plugins", []):
            logging.info(f"Loading {plugin}")
            dir_name, file_name, class_name = plugin.split(".")
            cls = getattr(
                import_module(f".plugins.{dir_name}.{file_name}", package=__package__),
                class_name,
            )
            plugins.append(cls(self.reddit, self.subreddit))
        return plugins

    def stream_subreddit(self):
        streams = self.config.get("streams", None)
        comment_stream = (
            self.subreddit.stream.comments(skip_existing=True, pause_after=-1)
            if streams.get("comments")
            else []
        )
        submission_stream = (
            self.subreddit.stream.submissions(skip_existing=True, pause_after=-1)
            if streams.get("submissions")
            else []
        )
        mod_stream = (
            self.subreddit.mod.stream.log(skip_existing=True, pause_after=-1)
            if streams.get("modlog")
            else []
        )
        modmail_stream = (
            self.subreddit.mod.stream.modmail_conversations(
                skip_existing=True, pause_after=-1
            )
            if streams.get("modmail")
            else []
        )
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
            for modmail in modmail_stream:
                if modmail is None:
                    break
                self.process_modmail(modmail)

    def process_comment(self, comment):
        for plugin in self.plugins:
            plugin.consume_comment(comment)

    def process_submission(self, submission):
        for plugin in self.plugins:
            plugin.consume_submission(submission)

    def process_mod_log(self, mod_log):
        for plugin in self.plugins:
            plugin.consume_mod_log(mod_log)

    def process_modmail(self, modmail):
        for plugin in self.plugins:
            plugin.consume_modmail(modmail)
