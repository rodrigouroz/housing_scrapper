import telegram
import logging
import random

class NullNotifier:
    def notify(self, properties):
        pass

class Notifier(NullNotifier):
    def __init__(self, config):
        logging.info(f"Setting up bot with token {config['token']}")
        self.config = config
        self.bot = telegram.Bot(token=self.config['token'])
        

    def notify(self, properties):
        logging.info(f'Notifying about {len(properties)} properties')
        text = random.choice(self.config['messages'])
        self.bot.send_message(chat_id=self.config['chat_id'], text=text)

        for prop in properties:
            logging.info(f"Notifying about {prop['url']}")
            self.bot.send_message(chat_id=self.config['chat_id'], 
                    text=f"[{prop['title']}]({prop['url']})",
                    parse_mode=telegram.ParseMode.MARKDOWN)

    @staticmethod
    def get_instance(config):
        if config['enabled']:
            return Notifier(config)
        else:
            return NullNotifier()