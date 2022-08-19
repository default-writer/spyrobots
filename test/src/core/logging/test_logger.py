# pylint: disable-msg=C0103
import logging

from unittest.mock import patch
from unittest import mock
from test.conftest import FakeLoggingWriter, FakeGetEnv, FakePathExists

from src.core.logging.logger import Log

messages = {
    'debug': [],
    'info': [],
    'warning': [],
    'error': [],
    'critical': []
}

class MockLoggingHandler(logging.Handler):
    """Mock logging handler to check for expected logs."""

    def __init__(self, *args, **kwargs):
        self.reset()
        logging.Handler.__init__(self, *args, **kwargs)

    def emit(self, record):
        self.messages[record.levelname.lower()].append(record.getMessage())

    def reset(self):
        self.messages = {
            'debug': [],
            'info': [],
            'warning': [],
            'error': [],
            'critical': [],
        }

    def get_messages(self, type):
        return self.messages[type]

def test_debug():
    log = Log(__name__)
    mocking_log_handler = MockLoggingHandler()
    log.add_handler(mocking_log_handler)
    messages = {
        'debug': 'debug message',
        'info': 'info message',
        'warning': 'warning message',
        'error': 'error message',
        'critical': 'critical message',
        'exception': 'exception message'
    }
    log.debug(messages['debug'])
    log.info(messages['info'])
    log.warning(messages['warning'])
    log.error(messages['error'])
    log.critical(messages['critical'])
    log.trace(messages['exception'])
    assert messages['debug'] in mocking_log_handler.get_messages('debug')
    assert messages['info'] in mocking_log_handler.get_messages('info')
    assert messages['warning'] in mocking_log_handler.get_messages('warning')
    assert messages['error'] in mocking_log_handler.get_messages('error')
    assert messages['critical'] in mocking_log_handler.get_messages('critical')
    assert messages['exception'] in mocking_log_handler.get_messages('error')


def test_logger_setup(logging):
    with patch("src.core.functions.os.getenv") as mock_getenv:
        mock_getenv.side_effect = FakeGetEnv({'LOG_CFG':'logging.yaml'})
        with patch("src.core.functions.os.path.isfile") as mock_isfile:
            mock_isfile.return_value = True
            with patch("src.core.functions.os.makedirs"):
                try:
                    Log.setup()
                except Exception:
                    assert False
        mock_getenv.stop()
    assert logging


def test_logger_cleanup(logging):
    with patch("src.core.functions.os.getenv") as mock_getenv:
        mock_getenv.side_effect = FakeGetEnv({'LOG_CFG':'logging.yaml'})
        with patch("src.core.functions.os.path.isfile") as mock_isfile:
            mock_isfile.return_value = True
            with patch("src.core.functions.os.makedirs"):
                try:
                    Log.setup()
                    Log.cleanup()
                except Exception:
                    assert False
        mock_getenv.stop()
    assert logging


def test_logger_setup_error(logging):
    with patch("src.core.functions.os.getenv") as mock_getenv:
        mock_getenv.side_effect = FakeGetEnv({'LOG_CFG':'logging.yaml'})
        with patch("src.core.functions.os.path.isfile") as mock_isfile:
            mock_isfile.return_value = True
            with patch("src.core.functions.os.makedirs") as mock_makedirs:
                mock_makedirs.side_effect = Exception()
                assert not Log.setup()
        mock_getenv.stop()
    assert logging


def test_logger_setup_not_exists(logging):
    with patch("src.core.functions.os.getenv") as mock_getenv:
        mock_getenv.side_effect = FakeGetEnv({'LOG_CFG':'logging.yaml'})
        with patch("src.core.functions.os.path.exists") as mock_exists:
            mock_exists.return_value = False
            with patch("src.core.functions.os.makedirs") as mock_makedirs:
                mock_makedirs.side_effect = Exception()
                assert Log.setup()
        mock_getenv.stop()
    assert logging


def test_logger_cleanup_not_exists(logging):
    with patch("src.core.functions.os.getenv") as mock_getenv:
        mock_getenv.side_effect = FakeGetEnv({'LOG_CFG':'logging.yaml'})
        with patch("src.core.functions.os.path.exists") as mock_exists:
            mock_exists.return_value = False
            with patch("src.core.functions.os.makedirs") as mock_makedirs:
                mock_makedirs.side_effect = Exception()
                try:
                    Log.cleanup()
                except Exception:
                    assert False
        mock_getenv.stop()
    assert logging


def test_logger_cleanup_exists(logging):
    with patch("src.core.functions.os.getenv") as mock_getenv:
        mock_getenv.side_effect = FakeGetEnv({'LOG_CFG':'logging.yaml'})
        with patch("src.core.functions.os.path.exists") as mock_exists:
            mock_exists.side_effect = FakePathExists()
            with patch("src.core.functions.os.makedirs") as mock_makedirs:
                mock_makedirs.side_effect = Exception()
                try:
                    Log.cleanup()
                except Exception:
                    assert False
        mock_getenv.stop()
    assert logging


def test_logger_cleanup_exists_noerror(logging):
    with patch("src.core.functions.os.getenv") as mock_getenv:
        mock_getenv.side_effect = FakeGetEnv({'LOG_CFG':'logging.yaml'})
        with patch("src.core.functions.os.path.exists") as mock_exists:
            mock_exists.return_value = True
            try:
                Log.cleanup()
            except Exception:
                assert False
        mock_getenv.stop()
    assert logging
