""" Test suite for the cli module.

The script can be executed on its own or incorporated into a larger test suite.
However the tests are run, be aware of which version of the package is actually
being tested. If the package is installed in site-packages, that version takes
precedence over the version in this project directory. Use a virtualenv test
environment or setuptools develop mode to test against the development version.

"""
from subprocess import check_output
from subprocess import STDOUT
from sys import executable

import pytest
from {{ cookiecutter.app_name }} import __version__
from {{ cookiecutter.app_name }}.cli import *  # tests __all__


def test_main(capsys):
    """ Test the main() function.

    """
    # Verify `--version` output as a basic sanity check.
    with pytest.raises(SystemExit) as exinfo:
        main(["--version"])
    assert 0 == exinfo.value.code
    _, stderr = capsys.readouterr()
    assert __version__ in stderr
    return


def test_script():
    """ Test command line execution.

    """
    # Verify `--version` output as a basic sanity check.
    cmdl = "{:s} -m {{ cookiecutter.app_name }}.cli --version".format(executable)
    assert __version__ in check_output(cmdl.split(), stderr=STDOUT)
    return
        

# Make the script executable.

if __name__ == "__main__":
    raise SystemExit(pytest.main(__file__))
