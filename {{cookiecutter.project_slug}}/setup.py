""" Setup script for the {{ cookiecutter.app_name }} application.

"""
from itertools import chain
from pathlib import Path

from setuptools import find_packages
from setuptools import setup


_config = {
    "name": "{{ cookiecutter.app_name }}",
    "author": "{{ cookiecutter.author_name }}",
    "author_email": "{{ cookiecutter.author_email }}",
    "url": "",
    "package_dir": {"": "src"},
    "packages": find_packages("src"),
    "entry_points": {
        "console_scripts": ("{{ cookiecutter.cli_script }} = {{ cookiecutter.app_name }}.cli:main",),
    },
    "data_files": ("etc/",),
}


def main():
    """ Execute the setup command.

    """
    def files(*dirs):
        """ Recursively list all files. """
        dirs = (Path(root).rglob("*") for root in dirs)
        return map(str, chain.from_iterable(dirs))

    def version():
        """ Get the local package version. """
        namespace = {}
        path = Path("src", _config["name"], "__version__.py")
        exec(path.read_text(), namespace)
        return namespace["__version__"]

    _config.update({
        "data_files": list(files(*_config["data_files"])),  # expand files
        "version": version(),
    })
    setup(**_config)
    return 0


# Make the script executable.

if __name__ == "__main__":
    raise SystemExit(main())
