import os
import signal

import logging

import telebot
from dotenv import load_dotenv

from helper import *
from message_handlers import init_bot_handlers

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

load_dotenv('.env')


class SignalHandler:
    shutdown_requested = False
    bot = None

    def __init__(self, bot):
        self.bot = bot
        signal.signal(signal.SIGINT, self.request_shutdown)
        signal.signal(signal.SIGTERM, self.request_shutdown)

    def request_shutdown(self, *args):
        print('Request to shutdown received, stopping')
        self.shutdown_requested = True
        bot.stop_polling()
        bot.stop_bot()
        bot.close()

    def can_run(self):
        return not self.shutdown_requested


if __name__ == '__main__':
    bot = telebot.TeleBot(os.getenv('TBOT_KEY'), parse_mode=None)  # You can set parse_mode by default. HTML or MARKDOWN
    init_bot_handlers(bot)
    bot.infinity_polling()
