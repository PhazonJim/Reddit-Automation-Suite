import os
import utils

class IndieSunday(utils.PluginBase):
    def __init__(self, reddit):
        CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.yaml")
        self.reddit = reddit
        self.config = utils.load_config(CONFIG_FILE)
        self.cache = utils.load_cache()
        self.hub = self.reddit.submission('roprhq')

    def consume_comment(self, comment):
        pass
    
    def consume_submission(self, submission):
        pass
    
    def consume_mod_log(self, mod_log):
        print(mod_log.target_permalink)
        if mod_log.action == 'removelink':
            self.remove_entry(mod_log.target_permalink)
        if mod_log.action == 'approvelink':
            self.add_entry(mod_log.target_permalink)

    def add_entry(self, permalink):
        url = 'https://www.reddit.com' + permalink
        submission = self.reddit.submission(url=url)
        if submission.link_flair_text == 'Indie Sunday':
            if submission.id not in self.posts:
                self.posts[submission.id] = {
                    'permalink': submission.permalink,
                    'title': submission.title
                }
                self.save_cached_submissions()
                self.update_hub()

    def remove_entry(self, permalink):
        url = 'https://www.reddit.com' + permalink
        submission = self.reddit.submission(url=url)
        if submission.link_flair_text == 'Indie Sunday':
            if submission.id in self.posts:
                del self.posts[submission.id]
                self.save_cached_submissions()
                self.update_hub()
    
    def update_hub(self):
        gameList = ''
        for post_id in self.posts:
            hyperlink = '[{}]({})'.format(self.posts[post_id]['title'], self.posts[post_id]['permalink'])
            gameList += '* {}\n'.format(hyperlink)
        body = '{}\n\n{}\n{}'.format(self.config["templateHeader"], gameList, self.config["templateFooter"])
        self.hub.edit(body)