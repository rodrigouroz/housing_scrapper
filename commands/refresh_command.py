from commands.base_command import BaseCommand

class RefreshCommand(BaseCommand):
    def run(self, update, context):
        update.message.reply_text(self.message_composer.get_refresh_message())
        exec(open("crawl.py").read())
        exec(open("notify.py").read())
