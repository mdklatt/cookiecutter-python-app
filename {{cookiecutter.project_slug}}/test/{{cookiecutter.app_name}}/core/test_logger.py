""" Test suite for the core.logger module.

The script can be executed on its own or incorporated into a larger test suite.
However the tests are run, be aware of which version of the package is actually
being tested. If the package is installed in site-packages, that version takes
precedence over the version in this project directory. Use a virtualenv test
environment or setuptools develop mode to test against the development version.

"""
from logging import DEBUG
from io import StringIO

import pytest

from {{ cookiecutter.app_name }}.core.logger import logger as _logger


@pytest.fixture
def logger():
    """ Get the global logger object for testing.

    """
    yield _logger
    _logger.stop()  # reset logger after each test
    return


class LoggerTest(object):
    """ Test suite for the Logger class.

    """
    def test_start(self, capsys, logger):
        """ Test the start method.

        """
        message = "test message"
        logger.start("debug")
        logger.debug(message)
        _, stderr = capsys.readouterr()
        assert logger.level == DEBUG
        assert message in stderr
        return

    def test_stop(self, capsys, logger):
        """ Test the stop() method.

        """
        logger.start("debug")
        logger.stop()
        logger.critical("test")
        _, stderr = capsys.readouterr()
        assert not stderr
        return

    def test_restart(self, capsys, logger):
        """ Test a restart.

        """
        debug_message = "debug message"
        logger.start("INFO")
        logger.debug(debug_message)
        _, stderr = capsys.readouterr()
        assert debug_message not in stderr
        logger.stop()
        logger.start("DEBUG")
        logger.debug(debug_message)
        _, stderr = capsys.readouterr()
        assert debug_message in stderr
        return

    def test_stream(self, logger):
        """ Test output to an alternate stream.

        """
        message = "test message"
        stream = StringIO()
        logger.start("debug", stream)
        logger.debug(message)
        assert message in stream.getvalue()
        return


# Make the module executable.

if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
