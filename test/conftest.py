import os
import json
import time
import pytest
import random

from dotenv.main import load_dotenv
from unittest.mock import Mock, patch
from src.core.utils import config_loader

TEST_ENVIRONMENT={'HOSTNAME':'hostname'}

from io import StringIO
from copy import deepcopy

def set_env():
    # Unit tests
    os.environ['HOSTNAME'] = 'hostname'

set_env()

def load_env():
    env = """
        HOSTNAME=server
    """
    load_dotenv(stream=StringIO(env))

class FakeTextIOWriter():
    def __enter__(self):
        return self
    def __exit__(self ,type, value, traceback):
        pass
    def read(self):
        file = """
            host:
                name: ${HOSTNAME}
        """
        return StringIO(file)

class NoMatchFakeTextIOWriter():
    def __enter__(self):
        return self
    def __exit__(self ,type, value, traceback):
        pass
    def read(self):
        file = """
            host:
                name: ${HOSTNAME}
        """
        return StringIO(file)


class FakeLoggingWriter():
    def __enter__(self):
        return self
    def __exit__(self ,type, value, traceback):
        pass
    def truncate(self):
        pass
    def seek(self, index, offset):
        pass
    def tell(self):
        return 0
    def read(self):
        file = """
version: 1

disable_existing_loggers: true

formatters:
  standard:
    format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  error:
    format: "%(asctime)s - %(name)s - %(levelname)s <PID %(process)d:%(processName)s> %(name)s.%(funcName)s(): %(message)s"

handlers:
  debug_file_handler:
    class: logging.handlers.RotatingFileHandler
    level: DEBUG
    formatter: standard
    filename: logs/debug.log
    maxBytes: 10485760 # 10MB
    backupCount: 20
    encoding: utf8
    mode: w

  root_file_handler:
    class: logging.handlers.RotatingFileHandler
    level: DEBUG
    formatter: standard
    filename: logs/logs.log
    maxBytes: 10485760 # 10MB
    backupCount: 20
    encoding: utf8
    mode: w

  console:
    class: logging.StreamHandler
    level: DEBUG
    formatter: standard
    stream: ext://sys.stdout

  error_console:
    class: logging.StreamHandler
    level: ERROR
    formatter: error
    stream: ext://sys.stderr

root:
  level: DEBUG
  handlers: [console, error_console, root_file_handler]
  propagate: yes

loggers:
  core.data.classes:
    level: DEBUG
    handlers: [console, error_console, debug_file_handler]
    propagate: yes
  core.kafka_manager:
    level: DEBUG
    handlers: [console, error_console, debug_file_handler]
    propagate: yes
  core.config:
    level: DEBUG
    handlers: [console, error_console, debug_file_handler]
    propagate: yes
  core.utils:
    level: DEBUG
    handlers: [console, error_console, debug_file_handler]
    propagate: yes
  core.blob_utils:
    level: DEBUG
    handlers: [console, error_console, debug_file_handler]
    propagate: yes
  core.file_utils:
    level: DEBUG
    handlers: [console, error_console, debug_file_handler]
    propagate: yes
  core.requests_utils:
    level: DEBUG
    handlers: [console, error_console, debug_file_handler]
    propagate: yes
        """
        return file
    def write(self, data):
        pass

class FakeGetEnv(dict):
    def __call__(self, key, default_value=None):
        return self[key] if key in self.keys() else default_value

class FakePathExists(object):
    def __call__(self, file_path):
        return not file_path.endswith('logs')

class NoEnvVarFakeTextIOWriter():
    def __enter__(self):
        return self
    def __exit__(self ,type, value, traceback):
        pass
    def read(self):
        file = """
            kafka:
                bootstrap.servers: ${BOOTSTRAP_SERVERS}
                sasl.username: ${KAFKA_USER}
                sasl.password: ${KAFKA_PASSWORD}
                security.protocol: ${KAFKA_SECURITY_PROTOCOL} #PLAINTEXT
                sasl.mechanisms: ${KAFKA_SASL_MECHANISMS} #PLAIN"
                ssl.ca.location: ${certifi} #certifi.where()
            oauth:
                token_url: ${TOKEN_URL}
                client_id: ${CLIENT_ID}
                client_secret: ${CLIENT_SECRET}
                client_scope: ${CLIENT_SCOPE}
                role: ${ROLE}
            endpoints:
                updated_provider_address_info:
                    endpoint: ${BLA}/?arg=updated_provider_address_info
                    topic:  ${BLA}
                updated_provider_address_info:
                    endpoint: ${ENDPOINT2}/?arg=updated_provider_address_info
                    topic:  ${TOPIC2}
        """
        return StringIO(file)


@pytest.fixture
def config():
    with patch("src.core.utils.load_dotenv") as mock_load_dotenv:
        mock_load_dotenv.side_effect = load_env
        with patch('builtins.open') as mock_builtins_open:
            mock_builtins_open.return_value = FakeTextIOWriter()
            yield config_loader()
            mock_builtins_open.stop()


@pytest.fixture
def config_error():
    with patch("app.core.utils.load_dotenv") as mock_load_dotenv:
        mock_load_dotenv.side_effect = load_env
        with patch('builtins.open') as mock_builtins_open:
            mock_builtins_open.return_value = NoEnvVarFakeTextIOWriter()
            yield config_loader()
            mock_builtins_open.stop()


@pytest.fixture
def logging():
    logging_patch = patch('builtins.open')
    mock = logging_patch.start()
    mock.return_value = FakeLoggingWriter()
    yield logging_patch
    logging_patch.stop()


def getenv(name):
    if name not in TEST_ENVIRONMENT:
        return None
    return TEST_ENVIRONMENT[name]