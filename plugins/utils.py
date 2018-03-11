import logging
import requests

logger = logging.getLogger('root')

def post_message(webhook, text, alias=None, channel=None, attachments=None):
    request_data = {
        'username': alias,
        'text': text,
    }
    if channel:
        request_data['channel'] = channel
    if attachments:
        request_data['attachments'] = attachments
    logger.debug('posting data: %s', request_data)
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

