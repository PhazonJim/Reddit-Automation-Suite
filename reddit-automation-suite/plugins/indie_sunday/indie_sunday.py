import os
import logging
from ...reddit_utils import PluginBase, get_permalink
from ...db.utils import add_or_update_indie_sunday, get_indie_sunday_posts

class IndieSunday(PluginBase):
    def __init__(self, reddit, subreddit):
        config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
        PluginBase.__init__(
            self,
            name="IndieSunday",
            reddit=reddit,
            subreddit=subreddit,
            config_path=config_path,
        )
        self.hub = self.get_current_hub()

    def consume_submission(self, submission):
        self.check_new_hubs(submission)

    def consume_mod_log(self, mod_log):
        self.check_submission_approvals_removals(mod_log)

    def update_hub(self):
        gameList = ""
        posts = get_indie_sunday_posts(self.hub.id)
        for post in posts:
            hyperlink = f"[{post.title}]({post.permalink})"
            gameList += f"* {hyperlink}\n".format()

        body = f"{self.config.get('templateHeader')}\n\n{gameList}\n{self.config.get('templateFooter')}"
        self.hub.edit(body)

    def get_current_hub(self):
        hub = list(self.subreddit.search(query="title:Indie Sunday Hub", sort="new"))[0]
        logging.info("Found Indie Sunday Hub: {}".format(hub.id))
        return hub

    def check_submission_approvals_removals(self, mod_log):
        permalink = get_permalink(mod_log.target_permalink)
        if not permalink:
            return
        submission = self.reddit.submission(url=permalink)
        if submission.link_flair_text == "Indie Sunday":
            if mod_log.action == "removelink":
                self.update_db_entries(submission, False)
            if mod_log.action == "approvelink":
                self.update_db_entries(submission, True)

    def check_new_hubs(self, submission):
        if (
            "Indie Sunday Hub" in submission.title
            and submission.author.name == "PhazonJim"
        ):
            self.hub = submission

    def update_db_entries(self, submission, status):
        verb = "Add" if status else "Remove"
        logging.info(f"{verb} Indie Sunday Post: {submission.permalink}")
        add_or_update_indie_sunday(submission, self.hub, status)
        self.update_hub()