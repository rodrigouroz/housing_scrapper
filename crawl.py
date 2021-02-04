#!/usr/bin/env python
from lib.config import Config
import yaml
import sys
from providers.processor import process_properties
from lib.debugger import run_debugger
import logging
from lib.logger_config import configure_logging
configure_logging(logging)

logging.info("Starting Crawler...")

# configuration
cfg = Config()

new_properties = []
for provider_name, provider_data in cfg.get('providers').items():
    try:
        logging.info(f"Processing provider {provider_name}")
        new_properties += process_properties(provider_name, provider_data)
    except:
        logging.error(f"Error processing provider {provider_name}.\n{sys.exc_info()[0]}")
        