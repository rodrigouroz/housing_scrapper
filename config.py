import yaml

class Config:
    def __init__(self):
        with open("configuration.yml", 'r') as ymlfile:
            self.cfg = yaml.safe_load(ymlfile)

    def get(self, section):
        return self.cfg[section]