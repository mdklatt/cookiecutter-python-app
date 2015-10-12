""" Test suite for the {{ cookiecutter.repo_name }} application.

The script can be executed on its own or incorporated into a larger test suite.
However the tests are run, be aware of which version of the package is actually
being tested. If the package is installed in site-packages, that version takes
precedence over the version in this project directory. Use a virtualenv test
environment or setuptools develop mode to test against the development version.

"""
from yaml import dump

import pytest


def test_version():
    """ Test the application version.

    """
    from {{ cookiecutter.repo_name }} import __version__
    assert "{{ cookiecutter.project_version }}" == __version__
    return


def test_main():
    """ Test the main entry point.

    """
    from {{ cookiecutter.repo_name }} import main
    with pytest.raises(NotImplementedError):
        main()
    return


def test_cli():
    """ Test the cli module.

    """
    from {{ cookiecutter.repo_name }}.cli import main
    with pytest.raises(NotImplementedError):
        main()
    return


def test_gui():
    """ Test the gui module.

    """
    from {{ cookiecutter.repo_name }}.gui import main
    with pytest.raises(NotImplementedError):
        main()
    return


def test_web():
    """ Test the web module.

    """
    from {{ cookiecutter.repo_name }}.web import main
    with pytest.raises(NotImplementedError):
        main()
    return


def test_logger(capsys):
    """ Test application logging.
    
    """
    from {{ cookiecutter.repo_name }}.core import LOGGER
    from {{ cookiecutter.repo_name }}.core import logger
    message = "core.logger test"
    LOGGER.critical(message)
    _, stderr = capsys.readouterr()
    assert not stderr  # no output until LOGGER is initialized
    logger("debug")
    LOGGER.debug(message)
    _, stderr = capsys.readouterr()
    assert message in stderr
    return


def test_config(tmpdir):
    """ Test application configuration.
    
    """
    from {{ cookiecutter.repo_name }}.core import CONFIG
    from {{ cookiecutter.repo_name }}.core import config
    configs = (
        (tmpdir.join("conf1.yml"), {"global": "conf1", "conf1": "conf1"}),
        (tmpdir.join("conf2.yml"), {"global": "conf2", "conf2": "conf2"}))
    for pathobj, data in configs:
        # Write config data to each config file.
        pathobj.write(dump(data))
    assert not CONFIG  # empty until loaded
    config(str(item[0]) for item in configs)
    assert {"global": "conf2", "conf1": "conf1", "conf2": "conf2"} == CONFIG
    return
    

# Make the module executable.

if __name__ == "__main__":
    raise SystemExit(pytest.main(__file__))
