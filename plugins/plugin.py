import logging
import time

logger = logging.getLogger('root')

class Plugin:
    plugins = []

    def __init_subclass__(cls, plugin, **kwargs):
        super().__init_subclass__(**kwargs)
        logger.info(f'Registering plugin {plugin}')
        cls.plugins.append(cls)
        cls.plugin = plugin

    def run(self):
        tasks = []
        if hasattr(self, 'loop'):
            tasks.append(self.loop)
        return tasks
