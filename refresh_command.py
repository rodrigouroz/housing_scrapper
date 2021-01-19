from config import Config
from telegram.ext import Updater, CommandHandler
from message_composer import MessageComposer

class RefreshCommand:
    def __init__(self):
        self.config = Config().get('notifier')
        self.message_composer = MessageComposer(self.config)
        updater = Updater(self.config['token'], use_context=True)
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("refresh", self.refresh))
        updater.start_polling()
        updater.idle()

    def refresh(self, update, context):
        update.message.reply_text(self.message_composer.get_refresh_message())
        exec(open("main.py").read())
