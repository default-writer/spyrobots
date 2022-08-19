# pylint: disable-msg=C0103
# pylint: disable-msg=W0703
import argparse
import json
import os
import sys

from dotenv import load_dotenv

from .core.logging.logger import Log
from .core.functions import get_current_time
from .core.utils import config_loader
from .core.logging.logger import Log

Log.setup(os.path.abspath(os.path.dirname(__file__)))

log = Log(__name__)


def get_args_from_command_line():
    log.debug("Creating argument parser for command line arguments")
    parser = argparse.ArgumentParser(description='shell runner')
    log.debug("Adding config command lined argument")
    parser.add_argument("-c", "--config", action="store", dest="config_file", default="config.yaml", help="Path to config file")
    log.debug("Adding robot virtual machine code file command lined argument")
    parser.add_argument("-v", "--virtual", action="store", dest="virtual_machine", default="local", help="Name of file to execute")

    log.debug("Parsing command lined arguments")
    pargs = parser.parse_args()
    return pargs


def error_handling():
    return f"Error: {sys.exc_info()[0]}. {sys.exc_info()[1]}, line: {sys.exc_info()[2].tb_lineno}"


def main():
    print("hello, world!")

if __name__ in ('__main__', 'src.main'):
    try:
        args = get_args_from_command_line()

        name = args.virtual_machine
        log.debug(f"File: {args.virtual_machine}")
        current_time = get_current_time()
        log.debug(f"Started at: {current_time}")

        file = args.config_file
        log.debug("Loading configuration")
        config = config_loader(default_file=file)
        host = config["host"]
        log.debug(f"Loading host: {json.dumps(host)}")

        if name in host['name']:
            main()

    except Exception as ex:
        message = str(ex)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        exc_type = exc_type.__name__ if exc_type else type(ex)
        exc_msg = f"{message}, {exc_type}: {exc_value}"  # type: ignore
        message = str(message)
        log.error(message)
        log.error(error_handling())
        sys.exit(1)
