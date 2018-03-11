import logging
import random
import requests
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger('default')

def post_message(webhook, text, alias=None, channel=None, attachments=None):
    request_data = {
        'username': alias,
        'text': text,
    }
    if channel:
        request_data['channel'] = channel
    if attachments:
        request_data['attachments'] = attachments
    requests.post(webhook, json=request_data)

def make_attachment(title, title_link, text, thumb_url=None, color=None):
    attachment = {
        'title': title,
        'title_link': title_link,
        'text': text
    }
    if thumb_url:
        attachment['thumb_url'] = thumb_url
        attachment['color'] = color
    return attachment


class Plugin:
    plugins = []

    def __init_subclass__(cls, plugin, **kwargs):
        print(f'Registering plugin {plugin}')
        cls.plugins.append(cls)
        cls.plugin = plugin

    @classmethod
    def _loop(cls, thing, *args, **kwargs):
        while True:
            getattr(cls, thing)(cls, *args, **kwargs)

    @classmethod
    def run(cls, *args, **kwargs):
        tasks = []
        if hasattr(cls, 'loop'):
            tasks.append((cls._loop, ('loop',) + args, kwargs))
        return tasks

class Bot:
    '''Main bot class'''
    def start(self):
        '''Start the bot'''
        plugins = Plugin.plugins
        with ThreadPoolExecutor() as e:
            futures = []
            for plugin in plugins:
                for task in plugin.run():
                    future = e.submit(task[0], *task[1], **task[2])
                    futures.append(future)
            while all([future.running() for future in futures]):
                print("All running")
                sleep(10)
            while any([future.running() for future in futures]):
                print("shutdown")
                e.shutdown()
