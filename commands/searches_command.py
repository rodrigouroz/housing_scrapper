from commands.base_command import BaseCommand

class SearchesCommand(BaseCommand):
    def run(self, update, context):
        self.config.load()
        search_index = 1
        providers_config = self.config.get('providers')
        for provider_key in providers_config.keys():
            messages = []
            messages.append(f"{provider_key.upper()}")
            provider_config = providers_config[provider_key]
            for source in provider_config['sources']:
                url = provider_config['base_url'] + source.replace('<', '%3C').replace('>', '%3E')
                messages.append(f"- [search number #{search_index}]({url})")
                search_index += 1
            provider_config_message = '\n'.join(messages)
            update.message.reply_markdown(provider_config_message)

