import yaml

class Config:
    def __init__(self):
        self.load()

    def load(self):
        with open("configuration.yml", 'r') as ymlfile:
            self.cfg = yaml.safe_load(ymlfile)

    def get(self, section):
        return self.cfg[section]

    def has(self, section):
        return section in self.cfg

    def get_disable_ssl(self):
        disable_ssl = False
        if self.has('disable_ssl'):
            disable_ssl = self.get('disable_ssl')
        return disable_ssl
