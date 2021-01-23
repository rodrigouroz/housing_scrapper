import logging
from telegram.ext import Updater, CommandHandler
from message_composer import MessageComposer
from lib.config import Config

from commands.refresh_command import RefreshCommand
from commands.searches_command import SearchesCommand

def run_debugger():
    import debugpy
    # 5678 is the default attach port in the VS Code debug configurations. Unless a host and port are specified, host defaults to 127.0.0.1
    debugpy.listen(5678)
    print("Waiting for debugger attach")
    debugpy.wait_for_client()
    debugpy.breakpoint()
    print('break on this line')

run_debugger()

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