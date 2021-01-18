import logging
import random
import webbrowser

import telegram


class NullNotifier:
    def notify(self, properties):
        pass

    @staticmethod
    def get_instance(config):
        if not config['enabled']:
            return NullNotifier()
        elif 'type' in config and 'browser'.__eq__(config['type'].lower()):
            return Browsifier(config)
        else:
            return Notifier(config)


class Notifier(NullNotifier):
    def __init__(self, config):
        logging.info(f"Setting up bot with token {config['token']}")
        self.config = config
        self.bot = telegram.Bot(token=self.config['token'])

    def notify(self, properties):
        logging.info(f'Notifying about {len(properties)} properties')
        text = random.choice(self.config['messages'])
        for user in self.config['chat_id']:
            self.bot.send_message(chat_id=user, text=text)

        for prop in properties:
            logging.info(f"Notifying about {prop['url']}")
            for user in self.config['chat_id']:
                self.bot.send_message(chat_id=user,
                                      text=f"[{prop['title']}]({prop['url']})",
                                      parse_mode=telegram.ParseMode.MARKDOWN)


class Browsifier(NullNotifier):
    def __init__(self, config):
        logging.info(f"Setting up notifier thru browser tabs")
        self.tabs_ = config['tabs'] if 'tabs' in config else 5

    def notify(self, properties):
        logging.info(f'Notifying about {len(properties)} properties')

        go = 'y'
        for props in self.chunks(properties, self.tabs_):
            if go:
                go = input(f"Open next {len(props)} tabs ?")
            for prop in props:
                if go == 'y':
                    webbrowser.open_new_tab(prop['url'])
                else:
                    logging.info(f"[{prop['title']}]({prop['url']})")

    @staticmethod
    def chunks(ppp, n):
        for i in range(0, len(ppp), n):
            yield ppp[i:i + n]
