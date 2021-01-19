from config import Config
from telegram.ext import Updater, CommandHandler

def refresh(update, context):
    update.message.reply_text("Actualizando propiedades disponibles...")
    exec(open("main.py").read())

def init():
    cfg = Config().get('notifier')
    updater = Updater(cfg['token'], use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("refresh", refresh))
    updater.start_polling()
    updater.idle()

init()
