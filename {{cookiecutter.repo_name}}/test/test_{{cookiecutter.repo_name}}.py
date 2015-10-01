""" Test suite for the {{ cookiecutter.repo_name }} application template.

The script can be executed on its own or incorporated into a larger test suite.
However the tests are run, be aware of which version of the package is actually
being tested. If the package is installed in site-packages, that version takes
precedence over the version in this project directory. Use a virtualenv test
environment or setuptools develop mode to test against the development version.

"""
import pytest


def test_version():
    """ Test the application version.

    """
    from {{ cookiecutter.repo_name }} import __version__
    assert __version__ == "{{ cookiecutter.project_version }}"
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


# Make the module executable.

if __name__ == "__main__":
    raise SystemExit(pytest.main(__file__))
