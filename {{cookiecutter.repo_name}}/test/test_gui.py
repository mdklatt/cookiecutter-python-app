""" Test suite for the cli module.

The script can be executed on its own or incorporated into a larger test suite.
However the tests are run, be aware of which version of the package is actually
being tested. If the package is installed in site-packages, that version takes
precedence over the version in this project directory. Use a virtualenv test
environment or setuptools develop mode to test against the development version.

"""
from subprocess import call
from subprocess import STDOUT
from sys import executable

import pytest
from {{ cookiecutter.app_name }} import __version__
from {{ cookiecutter.app_name }}.gui import *  # tests __all__


def test_main(capsys):
    """ Test the main() function.

    """
    assert 0 == main()
    return


def test_script():
    """ Test command line execution.

    """
    cmdl = "{:s} -m {{ cookiecutter.app_name }}.gui".format(executable)
    assert 0 == call(cmdl.split())
    return
        

# Make the module executable.

if __name__ == "__main__":
    raise SystemExit(pytest.main(__file__))
