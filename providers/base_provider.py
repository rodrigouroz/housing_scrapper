import logging
import cloudscraper
from abc import ABC, abstractmethod
from providers.hostname_ignoring_adapter import HostNameIgnoringAdapter
import yaml

# configuration
with open("configuration.yml", 'r') as ymlfile:
    print('loading config')
    cfg = yaml.safe_load(ymlfile)

disable_ssl = False

if 'disable_ssl' in cfg:
    disable_ssl = cfg['disable_ssl']
class BaseProvider(ABC):
    def __init__(self, provider_name, provider_data):
        self.provider_name = provider_name
        self.provider_data = provider_data
        self.__scraper = cloudscraper.create_scraper()
        if disable_ssl:
            self.__scraper.mount('https://', HostNameIgnoringAdapter())

    @abstractmethod
    def props_in_source(self, source):
        pass

    def request(self, url, allow_redirects=True):
        return self.__scraper.get(url, allow_redirects=allow_redirects, verify=not disable_ssl)

    def next_prop(self):
        for source in self.provider_data['sources']:
            logging.info(f'Processing source {source}')
            yield from self.props_in_source(source)
