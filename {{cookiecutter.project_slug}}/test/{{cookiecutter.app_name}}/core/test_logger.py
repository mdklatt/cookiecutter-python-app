""" Test suite for the core._logger module.

The script can be executed on its own or incorporated into a larger test suite.
However the tests are run, be aware of which version of the package is actually
being tested. If the package is installed in site-packages, that version takes
precedence over the version in this project directory. Use a virtualenv test
environment or setuptools develop mode to test against the development version.

"""
from logging import DEBUG
from logging import ERROR
from io import StringIO
from weakref import ref

import pytest
from {{ cookiecutter.app_name }}.core.logger import *  # tests __all__


@pytest.fixture
def smtp(monkeypatch):
    """ Mock the smtplib.SMTP class for testing.

    """
    class SMTP(object):
        """ Mock SMTP class. 
        
        """
        messages = []

        def __init__(self, *_, **__):
            """ Initialize this object. """
            for method in "ehlo", "login", "starttls", "quit":
                # Define dummy methods.
                setattr(self, method, lambda *_: None)
            return

        def send_message(self, msg):
            """ Queue the sent message for inspection. """
            self.messages.append(msg)
            return

    # This requires knowledge of the internal alias for smtplib.SMTP in the 
    # core.logger module.
    monkeypatch.setattr("{{ cookiecutter.app_name }}.core.logger.SMTP", SMTP)
    return SMTP.messages


class EmailHandlerTest(object):
    """ Test suite for the EmailHandler class.

    """
    def test_handler(self, smtp):
        """ Testing....
        
        """
        logger = Logger()
        handler = EmailHandler("host", "from", ["to1", "to2"], "testing")
        handler.setLevel(ERROR)
        logger.start()
        logger.addHandler(handler)
        logger.debug("debug")
        logger.error("error")
        logger.critical("critical")
        handler.flush()
        #handler.close()  # FIXME: doesn't call flush?
        del handler  # doesn't work because logger retains reference
        records = smtp[0].get_content().split("\n")
        assert all(x in y for (x, y) in zip(("error", "critical"), records))
        return


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
