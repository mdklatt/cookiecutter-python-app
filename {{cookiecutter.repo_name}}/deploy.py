""" Deploy the {{ cookiecutter.app_name }} application.

The project will be cloned from a Git repo and installed into a self-contained
virtualenv environment. By default the repo's master branch is deployed, but an
optional branch, tag, or commit can be specified. The resulting deployment will
have it's own complete set of Python libraries.

The deployment machine must have Python 2.7, pip, and virtualenv installed.

"""
from argparse import ArgumentParser
from contextlib import contextmanager
from os import chdir
from os import getcwd
from os.path import join
from shutil import rmtree
from sys import argv
from subprocess import check_call
from tempfile import mkdtemp


NAME = "{{ cookiecutter.app_name }}"
REPO = None 


def main():
    """ Script execution.

    The project repo will be cloned to a temporary directory, and the desired
    branch, tag, or commit will be checked out. Then, the application will be
    installed into a self-contained virtualenv environment.

    """
    @contextmanager
    def chwdir(path):
        """ Temporarily change the working directory. """
        cwd = getcwd()
        chdir(path)
        try:
            yield
        finally:
            chdir(cwd)
        return

    @contextmanager
    def tmpdir():
        """ Create a self-deleting temporary directory. """
        path = mkdtemp()
        try:
            yield path
        finally:
            rmtree(path)
        return

    parser = ArgumentParser()
    parser.add_argument("--repo", default=REPO,
        help="source repo [{:s}]".format(REPO))
    parser.add_argument("--checkout", default="master",
        help="branch, tag, or commit to use [master]")
    parser.add_argument("root", help="root path for the virtualenv")
    args = parser.parse_args(argv[1:])

    with tmpdir() as tmp:
        git = "git clone {:s} {:s}".format(args.repo, tmp)
        check_call(git.split())
        with chwdir(tmp):
            git = "git checkout {:s}".format(args.checkout)
            check_call(git.split())
        path = join(args.root, NAME)
        venv = "virtualenv {:s}".format(path)
        check_call(venv.split())
        with chwdir(path):
            pip = "bin/pip install -r {0:s}/requirements.txt {0:s}".format(tmp)
            check_call(pip.split())

    return 0


# Make the script executable.

if __name__ == "__main__":
    raise SystemExit(main())
