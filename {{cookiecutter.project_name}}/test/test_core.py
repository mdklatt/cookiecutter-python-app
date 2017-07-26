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


def test_logger_stderr(capsys):
    """ Test application logging to stderr.
    
    """
    message = "test_logger"
    logger.critical(message)
    _, stderr = capsys.readouterr()
    assert not stderr  # no output until logger is started
    logger.start("debug")
    try:
        assert logger.level == DEBUG
        logger.critical(message)
    finally:
        logger.stop()
    _, stderr = capsys.readouterr()
    assert not logger.active
    assert message in stderr
    return


def test_logger_stream():
    """ Test application logging to a stream.
    
    """
    message = "test_logger_stream"
    stream = BytesIO()
    logger.start("debug", stream)
    try:
        assert logger.level == DEBUG
        logger.critical(message)
    finally:
        logger.stop()
    assert not logger.active
    assert message in stream.getvalue()
    return
    
    
def test_config(tmpdir):
    """ Test application configuration.
    
    """
    configs = (
        (tmpdir.join("empty.yml"), None),
        (tmpdir.join("conf1.yml"), {"global": "%x1;", "%x1;": "%x1;"}),
        (tmpdir.join("conf2.yml"), {"global": "%x2;", "%x2;": "%x2;"}),
    )
    for pathobj, data in configs:
        # Write config data to each config file.
        pathobj.write(dump(data))
    assert not config  # empty until loaded
    params = {"x1": "conf1", "x2": "conf2"}
    merged = {"global": "conf2", "conf1": "conf1", "conf2": "conf2"}
    config.load((str(item[0]) for item in configs), params)
    try:
        # TODO: Need to test nested values.
        assert config == merged
        assert config["conf1"] == "conf1"  # item access
        assert config.conf1 == "conf1"  # attribute access
    finally:
        config.clear()
    return
    

# Make the module executable.

if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
