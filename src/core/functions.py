# pylint: disable-msg=C0103
# pylint: disable-msg=C0411
# pylint: disable-msg=E0401
import os
import json
import time

from .logging.logger import Log

log = Log(__name__)

def get_current_time():
    log.debug("Getting last access time")
    return int(time.time())
