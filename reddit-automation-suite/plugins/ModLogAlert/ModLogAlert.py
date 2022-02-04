import os
import praw
import textwrap
from discord_webhook import DiscordWebhook
import utils


class ModLogAlert(utils.PluginBase):
    def __init__(self, reddit, subreddit):
        self.reddit = reddit
        self.subreddt = subreddit
        self.config = utils.load_config(
            os.path.join(os.path.dirname(__file__), "config.yaml")
        )
        self.posts = []

    def consume_mod_log(self, mod_log):
        if mod_log.mod_reports:
            for report in mod_log.mod_reports:
                for phrase in self.config["report_config"]:
                    if phrase.lower() in report[0].lower():
                        self.post_webhook(mod_log, report, phrase)

    def post_webhook(self, mod_log, report, phrase):
        is_submission = isinstance(mod_log, praw.models.Submission)
        recipient = self.config["report_config"][phrase]["recipient"]
        webhook = self.config["report_config"][phrase]["webhook"]
        message = ""
        if recipient:
            message += "**Recipient:** {}\n".format(recipient)
        if report:
            message += "**Report:** {}\n".format(
                textwrap.shorten(
                    report[0],
                    width=1000,
                    placeholder="...(Too long to preview full content)...",
                )
            )
        if is_submission:
            message += "**Submission Title:** {}\n".format(mod_log.title)
            if mod_log.selftext:
                message += "**Content:** {}\n".format(
                    textwrap.shorten(
                        mod_log.selftext,
                        width=500,
                        placeholder="...(Too long to preview full content)...",
                    )
                )
        else:
            if mod_log.body:
                message += "**Content:** {}\n".format(
                    textwrap.shorten(
                        mod_log.body,
                        width=1000,
                        placeholder="...(Too long to preview full content)...",
                    )
                )
        message += "**Author:** {}\n".format(mod_log.author.name)
        message += "**Permalink:** https://www.reddit.com{}\n".format(mod_log.permalink)
        webhook = DiscordWebhook(url=webhook, content=message)
        webhook.execute()
