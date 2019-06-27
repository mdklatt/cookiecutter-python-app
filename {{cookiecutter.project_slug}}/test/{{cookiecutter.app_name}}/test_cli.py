""" Test suite for the cli module.

The script can be executed on its own or incorporated into a larger test suite.
However the tests are run, be aware of which version of the module is actually
being tested. If the library is installed in site-packages, that version takes
precedence over the version in this project directory. Use a virtualenv test
environment or setuptools develop mode to test against the development version.

"""
from subprocess import call
from sys import executable

import pytest
from {{ cookiecutter.app_name }}.cli import *  # test __all__


@pytest.fixture(params=("hello",))
def command(request):
    """ Return the command to run.

    """
    return request.param


def test_main(command):
    """ Test the main() function.

    """
    # Call with the --help option as a basic sanity check.
    with pytest.raises(SystemExit) as exinfo:
        main(("{:s}".format(command), "--help"))
    assert 0 == exinfo.value.code
    return


def test_script(command):
    """ Test command line execution.

    """
    # Call with the --help option as a basic sanity check.
    cmdl = "{:s} -m {{ cookiecutter.app_name }}.cli {:s} --help".format(executable, command)
    assert 0 == call(cmdl.split())
    return


# Make the script executable.

if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
