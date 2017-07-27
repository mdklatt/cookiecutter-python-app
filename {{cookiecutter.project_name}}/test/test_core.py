""" Test suite for the core.py module.

The script can be executed on its own or incorporated into a larger test suite.
However the tests are run, be aware of which version of the package is actually
being tested. If the package is installed in site-packages, that version takes
precedence over the version in this project directory. Use a virtualenv test
environment or setuptools develop mode to test against the development version.

"""
from logging import DEBUG
from io import BytesIO
from yaml import dump

import pytest
from {{ cookiecutter.app_name }}.core import *  # tests __all__


class LoggerTest(object):
    """ Test suite for the logger object.
    
    """
    @classmethod
    @pytest.fixture
    def reset(cls):
        """ Reset the logger object after each test.

        """
        yield
        logger.stop()
        return

    @pytest.mark.usefixtures("reset")
    def test_stop(self, capsys):
        """ Test the stop() method.
        
        """
        logger.stop()
        logger.critical("test")
        _, stderr = capsys.readouterr()
        assert not logger.active
        assert not stderr
        return
        
    @pytest.mark.usefixtures("reset")
    def test_start(self, capsys):
        """ Test the start method.
        
        """
        message = "test message"
        logger.start("debug")
        logger.debug(message)
        _, stderr = capsys.readouterr()
        assert logger.level == DEBUG
        assert message in stderr
        return

    @pytest.mark.usefixtures("reset")
    def test_stream(self):
        """ Test output to an alternate stream.
        
        """
        message = "test message"
        stream = BytesIO()
        logger.start("debug", stream)
        logger.debug(message)
        assert message in stream.getvalue()
        return
    
    
class ConfigTest(object):
    """ Test suite for the config object.

    """
    @classmethod
    @pytest.fixture
    def reset(cls):
        """ Reset the config object after each test.

        """
        yield
        config.clear()
        return

    @classmethod
    @pytest.fixture
    def files(cls, tmpdir):
        """ Write config files for testing.

        """
        configs = (
            (tmpdir.join("empty.yml"), None),
            (tmpdir.join("conf1.yml"), {"global": "%x1;", "%x1;": "%x1;"}),
            (tmpdir.join("conf2.yml"), {"global": "%x2;", "%x2;": "%x2;"}),
        )
        for pathobj, values in configs:
            pathobj.write(dump(values))
        return tuple(pathobj.strpath for pathobj, _ in configs)

    @pytest.mark.usefixtures("reset")
    def test_item(self):
        """ Test item access.

        """
        config["root"] = {}
        config["root"]["key"] = "value"
        assert config["root"]["key"] == "value"
        return

    @pytest.mark.usefixtures("reset")
    def test_attr(self):
        """ Test attribute access.

        """
        config.root = {}
        config.root.key = "value"
        assert config.root.key == "value"
        return

    @pytest.mark.usefixtures("reset")
    def test_load(self, files):
        """ Test the load() method.

        """
        merged = {"global": "conf2", "conf1": "conf1", "conf2": "conf2"}
        params = {"x1": "conf1", "x2": "conf2"}
        config.load(files, params)
        assert config == merged
        return
    

# Make the module executable.

if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
