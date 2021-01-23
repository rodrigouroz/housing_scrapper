#!/usr/bin/env python

import logging
from lib.logger_config import configure_logging
configure_logging(logging)

from commands.listener import Listener

command_listener = Listener()

command_listener.listen()