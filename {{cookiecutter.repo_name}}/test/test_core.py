""" Test suite for the core.py module.

The script can be executed on its own or incorporated into a larger test suite.
However the tests are run, be aware of which version of the package is actually
being tested. If the package is installed in site-packages, that version takes
precedence over the version in this project directory. Use a virtualenv test
environment or setuptools develop mode to test against the development version.

"""
from yaml import dump

import pytest
from {{ cookiecutter.repo_name }}.core import logger
from {{ cookiecutter.repo_name }}.core import config


def test_logger(capsys):
    """ Test application logging.
    
    """
    message = "core.logger test"
    logger.critical(message)
    _, stderr = capsys.readouterr()
    assert not stderr  # no output until logger is started
    logger.start("debug")
    logger.critical(message)
    _, stderr = capsys.readouterr()
    assert message in stderr
    logger.stop()
    return


def test_config(tmpdir):
    """ Test application configuration.
    
    """
    configs = (
        (tmpdir.join("conf1.yml"), {"global": "conf1", "conf1": "conf1"}),
        (tmpdir.join("conf2.yml"), {"global": "conf2", "conf2": "conf2"}))
    for pathobj, data in configs:
        # Write config data to each config file.
        pathobj.write(dump(data))
    assert not config  # empty until loaded
    config.load(str(item[0]) for item in configs)
    assert {"global": "conf2", "conf1": "conf1", "conf2": "conf2"} == config
    return
    

# Make the module executable.

if __name__ == "__main__":
    raise SystemExit(pytest.main(__file__))
