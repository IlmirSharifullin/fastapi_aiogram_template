import logging
import os

import requests

from src.settings import settings


def log_to_channel(msg, type='info'):
    if settings.logger.channel_id != '':
        res = requests.post(settings.logger.build_url(),
                            params={'text': ('ERROR:\n' if type == 'error' else 'INFO:\n') + str(msg)[-2000:],
                                    'chat_id': settings.logger.channel_id})
        return res.content


class CustomLogger(logging.Logger):
    def info(self, msg, *args, to_channel=False, **kwargs):
        super().info(msg, *args, **kwargs)
        if to_channel:
            res = log_to_channel(msg, 'info')

    def error(self, msg, *args, to_channel=True, **kwargs):
        super().error(msg, *args, **kwargs)
        if to_channel:
            res = log_to_channel(msg, 'error')


def setup_logger():
    logging.basicConfig(level=settings.logger.level,
                        format='%(asctime)s - %(levelname)s - %(name)s- %(message)s')

    return CustomLogger(__name__)

