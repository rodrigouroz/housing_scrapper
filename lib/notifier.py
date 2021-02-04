from message_composer import MessageComposer
import telegram
import logging
import random
from lib.sslless_session import SSLlessSession
import yaml
from lib.dao import Dao

class NullNotifier:
    def notify(self, properties):
        pass

class Notifier(NullNotifier):
    def __init__(self, config, disable_ssl):
        self.dao = Dao()
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
        self.__send_message(self.message_composer.get_good_message())
        for prop in properties:
            logging.info(f"Notifying about {prop['url']}")
            try:
                self.__send_markdown_message(Notifier.get_prop_markdown(prop))
                self.dao.mark_as_notified(prop)
            except:
                self.failed.append(prop)

    def __send_message(self, message):
        self.bot.send_message(chat_id=self.config['chat_id'], text=message)

    @staticmethod
    def get_prop_markdown(prop):
        return f"[{prop['title']}]({prop['url']})"

    @staticmethod
    def get_instance(config, disable_ssl = False):
        if config['enabled']:
            return Notifier(config, disable_ssl)
        else:
            return NullNotifier()

    def __send_markdown_message(self, message):
        self.bot.send_message(chat_id=self.config['chat_id'], 
                text=message,
                parse_mode=telegram.ParseMode.MARKDOWN)

    def bad_news(self):
        self.__send_markdown_message(self.message_composer.get_bad_message())

    def get_failed(self):
        return self.failed
