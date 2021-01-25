from commands.base_command import BaseCommand

class SearchesCommand(BaseCommand):
    def run(self, update, context):
        self.config.load()
        providers_config = self.config.get('providers')
        for provider_key in providers_config.keys():
            messages = []
            messages.append(f"> {provider_key}:")
            provider_config = providers_config[provider_key]
            for source in provider_config['sources']:
                url = provider_config['base_url'] + source
                messages.append(f">>> {url}")
            provider_config_message = '\n'.join(messages)
            update.message.reply_text(provider_config_message)

