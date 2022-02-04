import os
import logging
from ...utils import PluginBase


class ModmailHelper(PluginBase):
    def __init__(self, reddit, subreddit):
        PluginBase.__init__(
            self,
            name="ModmailHelper",
            reddit=reddit,
            subreddit=subreddit,
            config_path=os.path.join(os.path.dirname(__file__), "config.yaml"),
        )

    def consume_modmail(self, modmail):
        logging.debug(f"From: {modmail.owner}, To: {modmail.participant}")
        message = f"Modmail from: /u/{modmail.participant},\n\n"
        recent_post = None
        recent_comment = None
        if modmail.user.recent_posts:
            recent_post = modmail.user.recent_posts[0]
        if modmail.user.recent_comments:
            recent_comment = modmail.user.recent_comment[0]
        if recent_post:
            if recent_post.removed_by_category:
                message += (
                    f"* Recent submission was removed by: {recent_post.banned_by}\n\n"
                )
                message += f"* Removal reason: {recent_post.link_flair_text}\n\n"
        if recent_comment:
            if recent_comment.removed_by_category:
                message += (
                    f"* Recent comment was removed by: {recent_comment.banned_by}\n\n"
                )
        if modmail.user.ban_status["isBanned"]:
            message += f"* User is currently banned by (Fill in with snoonote API)"
        modmail.reply(message, internal=True)
