""" Test suite for the cli module.

The script can be executed on its own or incorporated into a larger test suite.
However the tests are run, be aware of which version of the module is actually
being tested. If the library is installed in site-packages, that version takes
precedence over the version in this project directory. Use a virtualenv test
environment or setuptools develop mode to test against the development version.

"""
from shlex import split
from subprocess import call
from sys import executable

import pytest
from {{ cookiecutter.app_name }}.cli import *  # test __all__


@pytest.fixture(params=("--help", "hello"))
def command(request):
    """ Return the command to run.

    """
    return request.param


def test_main(command):
    """ Test the main() function.

    """
    try:
        status = main(split(command))
    except SystemExit as ex:
        status = ex.code
    assert status == 0
    return

def test_main_none():
    """ Test the main() function with no arguments.
    
    """
    with pytest.raises(SystemExit) as exinfo:
        main([])  # displays a help message and exits gracefully
    assert exinfo.value.code == 1


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
