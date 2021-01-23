import logging
from telegram.ext import Updater, CommandHandler
from message_composer import MessageComposer
from lib.config import Config

from commands.refresh_command import RefreshCommand
from commands.searches_command import SearchesCommand

import lib.debugger

class Listener:
    def __init__(self):
        self.config = Config()
        self.notifier_config = self.config.get('notifier')
        self.message_composer = MessageComposer(self.notifier_config)
        self.commands = {
            'refresh': RefreshCommand,
            'searches': SearchesCommand
        }
        self.updater = Updater(self.notifier_config['token'], use_context=True)
        self.dispatcher = self.updater.dispatcher
    
    def listen(self):
        logging.info("Initializing commands...")
        for key in self.commands.keys():
            logging.info(f"Loading command listener for {key} command")
            command = self.commands[key](self.message_composer, self.config)
            self.dispatcher.add_handler(CommandHandler(key, command.run))
        self.updater.start_polling()
        self.updater.idle()