import logging
from abc import ABC, abstractmethod

class BaseProvider(ABC):
    def __init__(self, provider_name, provider_data):
        self.provider_name = provider_name
        self.provider_data = provider_data
    
    @abstractmethod
    def props_in_source(self, source):
        pass

    def next_prop(self):
        for source in self.provider_data['sources']:
            logging.info(f'Processing source {source}')
            yield from self.props_in_source(source)