# pylint: disable-msg=C0103
# pylint: disable-msg=W0703
# pylint: disable=invalid-name
import logging
import logging.config
import os
import coloredlogs
import yaml

from string import Formatter

log = logging.getLogger(__name__)


class Log:

    def __init__(self, name, logging_level=logging.DEBUG):
        self.fmt = Formatter()
        print(f"Setup logger {name}")
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging_level)

    @staticmethod
    def setup(default_path='.', default_file="logging.yaml", env_key='LOG_CFG', default_level=logging.DEBUG):
        try:
            value = os.getenv(env_key, None)
            if value:
                default_path = value
            path = os.path.abspath(default_path)
            file = os.path.join(path, default_file)
            if not os.path.exists(file):
                file = os.path.join(os.path.abspath(os.path.dirname(__file__)), default_file)
            if os.path.exists(file):
                with open(file, 'rt', encoding='utf-8') as file_handle:
                    config = yaml.safe_load(file_handle.read())
                    if 'handlers' in config and isinstance(config['handlers'], dict):
                        for _, section in config['handlers'].items():
                            if 'filename' in section:
                                section['filename'] = os.path.join(path, section['filename'])
                                full_path = os.path.dirname(section['filename'])
                                if not os.path.exists(full_path):
                                    os.makedirs(full_path)
                    logging.config.dictConfig(config)
                    coloredlogs.install()
                    return True
            else:
                logging.basicConfig(level=default_level)
                coloredlogs.install(level=default_level)
                print(f"File not found {file}")
                print('Failed to load configuration file. Using default configs')
                return True

        except Exception as ex:
            print(ex)
            print('Error in Logging Configuration. Using default configs')
            logging.basicConfig(level=default_level)
            coloredlogs.install(level=default_level)
            return False

    @staticmethod
    def cleanup(default_path='.', default_file="logging.yaml", env_key='LOG_CFG'):
        value = os.getenv(env_key, None)
        if value:
            default_path = value
        path = os.path.abspath(os.path.dirname(default_path))
        file = os.path.join(path, default_file)
        if not os.path.exists(file):
            file = os.path.join(os.path.abspath(os.path.dirname(__file__)), default_file)
        if os.path.exists(file):
            with open(file, 'rt', encoding='utf-8') as file_handle:
                config = yaml.safe_load(file_handle.read())
                if 'handlers' in config:
                    for _, section in config['handlers'].items():
                        if 'filename' in section:
                            try:
                                if os.path.exists(os.path.dirname(os.path.join(path, section['filename']))):
                                    section['filename'] = os.path.join(path, section['filename'])
                                    with open(section['filename'], 'w', encoding='utf-8') as file_log:
                                        file_log.truncate()
                                else:
                                    os.makedirs(os.path.dirname(os.path.join(path, section['filename'])))
                            except Exception as ex:
                                print(ex)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg if not args and not kwargs else self.fmt.format(msg, *args, **kwargs))

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg if not args and not kwargs else self.fmt.format(msg, *args, **kwargs))

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg if not args and not kwargs else self.fmt.format(msg, *args, **kwargs))

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg if not args and not kwargs else self.fmt.format(msg, *args, **kwargs))

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg if not args and not kwargs else self.fmt.format(msg, *args, **kwargs))

    def trace(self, msg, *args, **kwargs):
        self.logger.exception(msg if not args and not kwargs else self.fmt.format(msg, *args, **kwargs))

    def add_handler(self, handler):
        self.logger.addHandler(handler)
