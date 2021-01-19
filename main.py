#!/usr/bin/env python

from config import Config
import logging
import yaml
import sys
from lib.notifier import Notifier
from providers.processor import process_properties

# logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# configuration
cfg = Config()

disable_ssl = False
if 'disable_ssl' in cfg:
    disable_ssl = cfg.get('disable_ssl')

notifier = Notifier.get_instance(cfg.get('notifier'), disable_ssl)

new_properties = []
for provider_name, provider_data in cfg.get('providers').items():
    try:
        logging.info(f"Processing provider {provider_name}")
        new_properties += process_properties(provider_name, provider_data)
    except:
        logging.error(f"Error processing provider {provider_name}.\n{sys.exc_info()[0]}")

if len(new_properties) > 0:
    notifier.notify(new_properties)
else:
    notifier.bad_news()