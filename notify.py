#!/usr/bin/env python
from lib.config import Config
import yaml
import sys
from lib.notifier import Notifier
from providers.processor import process_properties
from lib.dao import Dao
from lib.debugger import run_debugger
import logging
from lib.logger_config import configure_logging
configure_logging(logging)

logging.info("Starting Notifier...")

# configuration
cfg = Config()

notifier = Notifier.get_instance(cfg.get('notifier'), cfg.get_disable_ssl())

dao = Dao()
new_properties = dao.get_pending_to_notify()

if len(new_properties) > 0:
    notifier.notify(new_properties)
else:
    notifier.bad_news()

failed_props = notifier.get_failed()

if (len(failed_props) > 0):
    failed_props = ', '.join([f"{prop['title']} - {prop['url']}" for prop in failed_props])
    logging.error(f"Failed notifying about this properties: {failed_props}")
