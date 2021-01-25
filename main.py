#!/usr/bin/env python
from lib.config import Config
import yaml
import sys
from lib.notifier import Notifier
from providers.processor import process_properties
from lib.dao import Dao
from lib.debugger import run_debugger
run_debugger()
import logging
from lib.logger_config import configure_logging
configure_logging(logging)

logging.info("Starting Crawler...")

# configuration
cfg = Config()

notifier = Notifier.get_instance(cfg.get('notifier'), cfg.get_disable_ssl())

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

failed_props = notifier.get_failed()

# FIXME: Added a deletion routine
#     that removes the failed-to-notify properties from DB
# IDEALLY: we could register the properties
#     with a new flag field `notified` in FALSE
#     And turn it to TRUE after being notified
#     with a separate python process
dao = Dao()
for prop in failed_props:
    dao.delete(prop)

if (len(failed_props) > 0):
    failed_props = ', '.join([f"{prop['title']} - {prop['url']}" for prop in failed_props])
    logging.error(f"Failed notifying about this properties: {failed_props}")
