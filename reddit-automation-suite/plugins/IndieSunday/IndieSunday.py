import os
import logging
from ...utils import PluginBase, get_full_permalink


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

    def add_entry(self, permalink):
        submission = self.reddit.submission(url=permalink)
        if submission.link_flair_text == "Indie Sunday":
            logging.info("Add Indie Sunday Post: {}".format(permalink))
            if submission.id not in self.cache[self.hub.id]:
                self.cache[self.hub.id][submission.id] = {
                    "permalink": submission.permalink,
                    "title": submission.title,
                }
                self.save_cache()
                self.update_hub()

    def remove_entry(self, permalink):
        submission = self.reddit.submission(url=permalink)
        if submission.link_flair_text == "Indie Sunday":
            logging.info("Remove Indie Sunday Post: {}".format(permalink))
            if submission.id in self.cache[self.hub.id]:
                del self.cache[self.hub.id][submission.id]
                self.save_cache()
                self.update_hub()

    def update_hub(self):
        gameList = ""
        posts = self.cache[self.hub.id]
        for post_id in posts:
            hyperlink = "[{}]({})".format(
                posts[post_id]["title"], posts[post_id]["permalink"]
            )
            gameList += "* {}\n".format(hyperlink)
        body = "{}\n\n{}\n{}".format(
            self.config["templateHeader"], gameList, self.config["templateFooter"]
        )
        self.hub.edit(body)

    def get_current_hub(self):
        hub = list(self.subreddit.search(query="title:Indie Sunday Hub", sort="new"))[0]
        logging.info("Found Indie Sunday Hub: {}".format(hub.id))
        if hub.id not in self.cache:
            self.cache[hub.id] = {}
        logging.debug("Current Cache: {}".format(self.cache))
        return hub

    def check_submission_approvals_removals(self, mod_log):
        permalink = get_full_permalink(mod_log.target_permalink)
        if mod_log.action == "removelink":
            self.remove_entry(permalink)
        if mod_log.action == "approvelink":
            self.add_entry(permalink)

    def check_new_hubs(self, submission):
        if (
            "Indie Sunday Hub" in submission.title
            and submission.author.name == "rGamesMods"
        ):
            self.hub = submission
            self.cache[submission.id] = {}