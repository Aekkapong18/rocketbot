import logging
import time
from concurrent.futures import ThreadPoolExecutor

from plugins import Plugin

logger = logging.getLogger('root')

class Bot:
    '''Main bot class'''

    def __init__(self):
        logger.debug('bot start')

    def start(self):
        '''Start the bot'''
        plugins = Plugin.plugins
        with ThreadPoolExecutor() as e:
            futures = []
            for plugin in plugins:
                for task in plugin().run():
                    future = e.submit(task)
                    futures.append(future)
            while all([future.running() for future in futures]):
                time.sleep(10)
            while any([future.running() for future in futures]):
                logger.info('Thread died, shutting down')
                print("shutdown")
                e.shutdown()
                time.sleep(10)
            logger.info("All threads are dead")
