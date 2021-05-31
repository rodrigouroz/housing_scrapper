#!/usr/bin/env python
import telegram
from lib.config import Config
bot_token = Config().get('notifier')['token']
bot = telegram.Bot(token=bot_token)
chat_ids = ', '.join([str(u.message.chat.id) for u in bot.get_updates()])
print(f"You can use this chat IDs in your configuration.yml file: {chat_ids}")
