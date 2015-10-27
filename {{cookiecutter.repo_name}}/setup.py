""" Setup script for the {{ cookiecutter.repo_name }} application.

"""
from distutils import log
from functools import partial
from os.path import join
from subprocess import check_call
from subprocess import CalledProcessError

from setuptools import Command
from setuptools import find_packages
from setuptools import setup


_ETC_FILES = {
    # Files are keyed by their project directory location and will be installed
    # into the same location under the Python installation path, e.g. the
    # application virtualenv environment.
    "etc": ("config.yml",),
}


_CONFIG = {
    "name": "{{ cookiecutter.repo_name }}",
    "author": "{{ cookiecutter.author_name }}",
    "author_email": "{{ cookiecutter.author_email }}",
    "url": "",
    "package_dir": {"": "src"},
    "packages": find_packages("src"),
    "entry_points": {
        "console_scripts": ("{{ cookiecutter.repo_name }}_cli = {{ cookiecutter.repo_name }}.cli:main",),
        "gui_scripts": ("{{ cookiecutter.repo_name }}_gui = {{ cookiecutter.repo_name }}.gui:main",)},
    "data_files": [(root, map(partial(join, root), paths)) for (root, paths)
                   in _ETC_FILES.iteritems()],
}


def version():
    """ Get the local package version.

    """
    path = join("src", _CONFIG["name"], "__version__.py")
    with open(path) as stream:
        exec(stream.read())
    return __version__


class _CustomCommand(Command):
    """ Abstract base class for a custom setup command.

    """
    # Each user option is a tuple consisting of the option's long name (ending
    # with "=" if it accepts an argument), its single-character alias, and a
    # description.
    description = ""
    user_options = []  # this must be a list

    def initialize_options(self):
        """ Set the default values for all user options.

        """
        return

    def finalize_options(self):
        """ Set final values for all user options.

        This is run after all other option assignments have been completed
        (e.g. command-line options, other commands, etc.)

        """
        return

    def run(self):
        """ Execute the command.

        Raise SystemExit to indicate failure.

        """
        raise NotImplementedError


class UpdateCommand(_CustomCommand):
    """ Custom setup command to pull from a remote branch.

    """
    description = "update from a remote branch"
    user_options = [
        ("remote=", "r", "remote name [default: tracking remote]"),
        ("branch=", "b", "branch name [default: tracking branch]"),
    ]

    def initialize_options(self):
        """ Set the default values for all user options.

        """
        self.remote = ""  # default to tracking remote
        self.branch = ""  # default to tracking branch
        return

    def run(self):
        """ Execute the command.

        """
        args = {"remote": self.remote, "branch": self.branch}
        cmdl = "git pull --ff-only {remote:s} {branch:s}".format(**args)
        try:
            check_call(cmdl.split())
        except CalledProcessError:
            raise SystemExit(1)
        log.info("package version is now {:s}".format(version()))
        return


class VirtualenvCommand(_CustomCommand):
    """ Custom setup command to create a virtualenv environment.

    """
    description = "create a virtualenv environment"
    user_options = [
        ("name=", "m", "environment name [default: venv]"),
        ("python=", "p", "Python interpreter"),
        ("requirements=", "r", "pip requirements file"),
    ]

    def initialize_options(self):
        """ Set the default values for all user options.

        """
        self.name = "venv"
        self.python = None  # default to version used to install virtualenv
        self.requirements = None
        return

    def run(self):
        """ Execute the command.

        """
        venv = "virtualenv {:s}"
        if self.python:
            venv += " -p {:s}"
        pip = "{0:s}/bin/pip install -r {2:s}" if self.requirements else None
        args = self.name, self.python, self.requirements
        try:
            check_call(venv.format(*args).split())
            if pip:
                log.info("installing requirements")
                check_call(pip.format(*args).split())
        except CalledProcessError:
            raise SystemExit(1)
        return


def main():
    """ Execute the setup commands.

    """
    _CONFIG["version"] = version()
    _CONFIG["cmdclass"] = {
        "virtualenv": VirtualenvCommand,
        "update": UpdateCommand,
    }
    setup(**_CONFIG)
    return 0


# Make the script executable.

if __name__ == "__main__":
    raise SystemExit(main())
