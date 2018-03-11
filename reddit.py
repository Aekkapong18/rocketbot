import logging
import time

import praw

from db import DataStore
from config import REDDIT_WEBHOOK
from common import post_message, make_attachment, Plugin

class Reddit(Plugin, plugin='reddit'):
    done = []
    def __init__(self):
        self.logger = logging.getLogger(name="reddit")
        self.done = DataStore.get(self.plugin, 'done')
        self.logger.error(self.done)
        print(self.done)
        if not self.done:
            DataStore.save(self.plugin, 'done', self.done)

    def loop(self):
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
