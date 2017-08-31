""" Test the python-app Cookiecutter template.

A template project is created in a temporary directory, the application is
installed into a self-contained virtualenv environment, and the application
test suite is run.

"""
from contextlib import contextmanager
from json import load
from os import chdir
from os import getcwd
from os.path import abspath
from os.path import dirname
from os.path import join
from shlex import split
from shutil import rmtree
from subprocess import check_call
from tempfile import mkdtemp
from venv import create

from cookiecutter.main import cookiecutter

def main():
    """ Execute the test.
    
    """
    @contextmanager
    def tmpdir():
        """ Enter a self-deleting temporary directory. """
        cwd = getcwd()
        tmp = mkdtemp()
        try:
            chdir(tmp)
            yield tmp
        finally:
            rmtree(tmp)
            chdir(cwd)
        return

    template = dirname(dirname(abspath(__file__)))
    defaults = load(open(join(template, "cookiecutter.json")))
    with tmpdir():
        cookiecutter(template, no_input=True)
        chdir(defaults["project_name"])
        create("venv", with_pip=True)
        install = "venv/bin/pip install ."
        for name in "requirements.txt", "test/requirements.txt":
            install = " ".join((install, "--requirement={:s}".format(name)))
        check_call(split(install))
        pytest = "venv/bin/pytest --verbose test"
        check_call(split(pytest))
    return 0
    
    
# Make the script executable.

if __name__ == "__main__":
    raise SystemExit(main())
