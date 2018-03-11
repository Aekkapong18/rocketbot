import log
log.setup_custom_logger('root')

from bot import Bot

from plugins import Reddit


bot = Bot()
bot.start()
