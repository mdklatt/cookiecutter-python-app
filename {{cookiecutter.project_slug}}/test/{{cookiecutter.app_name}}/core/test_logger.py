""" Test suite for the core._logger module.

The script can be executed on its own or incorporated into a larger test suite.
However the tests are run, be aware of which version of the package is actually
being tested. If the package is installed in site-packages, that version takes
precedence over the version in this project directory. Use a virtualenv test
environment or setuptools develop mode to test against the development version.

"""
from logging import DEBUG
from io import StringIO

import pytest
from {{ cookiecutter.app_name }}.core.logger import *  # tests __all__


class LoggerTest(object):
    """ Test suite for the Logger class.
    
    """
    def test_start(self, capsys):
        """ Test the start method.
        
        """
        message = "test message"
        logger = Logger()
        logger.start("debug")
        logger.debug(message)
        _, stderr = capsys.readouterr()
        assert logger.level == DEBUG
        assert message in stderr
        return

    def test_stop(self, capsys):
        """ Test the stop() method.
        
        """
        logger = Logger()
        logger.start("debug")
        logger.stop()
        logger.critical("test")
        _, stderr = capsys.readouterr()
        assert not stderr
        return

    def test_stream(self):
        """ Test output to an alternate stream.
        
        """
        message = "test message"
        stream = StringIO()
        logger = Logger()
        logger.start("debug", stream)
        logger.debug(message)
        assert message in stream.getvalue()
        return


# Make the module executable.

if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
