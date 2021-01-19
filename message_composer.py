import random

class MessageComposer:
    def __init__(self, config):
        self.config = config

    def __get_random(self, key):
        return random.choice(self.config[key])

    def get_good_message(self):
        return self.__get_random('good_news_messages')

    def get_bad_message(self):
        return self.__get_random('bad_news_messages')

    def get_refresh_message(self):
        return self.__get_random('refresh_command_messages')