from message_composer import MessageComposer
import telegram
import logging
import random
from lib.sslless_session import SSLlessSession
import yaml

class NullNotifier:
    def notify(self, properties):
        pass

class Notifier(NullNotifier):
    def __init__(self, config, disable_ssl):
        self.failed = []
        logging.info(f"Setting up bot with token {config['token']}")
        self.config = config
        if disable_ssl:
            self.bot = telegram.Bot(token=self.config['token'], request=SSLlessSession())
        else:
            self.bot = telegram.Bot(token=self.config['token'])
        self.message_composer = MessageComposer(config)        

    def notify(self, properties):
        logging.info(f'Notifying about {len(properties)} properties')
        self.bot.send_message(chat_id=self.config['chat_id'], text=self.message_composer.get_good_message())
        for prop in properties:
            logging.info(f"Notifying about {prop['url']}")
            try:
                self.bot.send_message(chat_id=self.config['chat_id'], 
                        text=f"[{prop['title']}]({prop['url']})",
                        parse_mode=telegram.ParseMode.MARKDOWN)
            except:
                self.failed.append(prop)

    def test(self, message):
        self.bot.send_message(chat_id=self.config['chat_id'], text=message)

    @staticmethod
    def get_instance(config, disable_ssl = False):
        if config['enabled']:
            return Notifier(config, disable_ssl)
        else:
            return NullNotifier()

    def bad_news(self):
        self.bot.send_message(chat_id=self.config['chat_id'], 
                text=self.message_composer.get_bad_message(),
                parse_mode=telegram.ParseMode.MARKDOWN)

    def get_failed(self):
        return self.failed
