class BaseCommand:
    def __init__(self, message_composer, config):
        self.config = config
        self.message_composer = message_composer

    def run(self, update, context):
        raise Exception("Command action not defined")