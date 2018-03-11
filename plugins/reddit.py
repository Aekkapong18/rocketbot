import logging
import time

import praw

from .db import DataStore
from .config import REDDIT_WEBHOOK, LOG_LEVEL
from .plugin import Plugin
from .utils import post_message, make_attachment

class Reddit(Plugin, plugin='reddit'):
    def __init__(self):
        self.logger = logging.getLogger('root')
        self.done = DataStore.get(self.plugin, 'done')
        self.logger.debug("processed messages: %s", ','.join(self.done))
        if not self.done:
            self.done = []
            DataStore.save(self.plugin, 'done', self.done)

    def loop(self):
        while True:
            try:
                r = praw.Reddit(user_agent='LineageOS Slack Bot v1.0')
                r.read_only = True
                for post in r.subreddit('lineageos').new(limit=10):
                    if post.id in self.done:
                        continue
                    attachment = make_attachment(title=post.title, title_link=post.url, text=post.selftext, thumb_url='https://www.redditstatic.com/icon.png')
                    post_message(REDDIT_WEBHOOK, post.url, alias='reddit', channel='#spam', attachments=[attachment])
                    self.done.append(post.id)
                    DataStore.save(self.plugin, 'done', self.done)
            except Exception as e:
                print(e)
                pass
            time.sleep(60)

if __name__ == '__main__':
    reddit = Reddit()
    reddit.loop()
