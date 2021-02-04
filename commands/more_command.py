from commands.base_command import BaseCommand

class MoreCommand(BaseCommand):
    def run(self, update, context):
        exec(open("notify.py").read())
