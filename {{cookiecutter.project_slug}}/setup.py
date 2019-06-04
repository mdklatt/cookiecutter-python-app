""" Setup script for the {{ cookiecutter.app_name }} application.

"""
from os import walk
from pathlib import Path

from setuptools import find_packages
from setuptools import setup


_config = {
    "name": "{{ cookiecutter.app_name }}",
    "url": "{{ cookiecutter.project_url }}",
    "author": "{{ cookiecutter.author_name }}",
    "author_email": "{{ cookiecutter.author_email }}",
    "package_dir": {"": "src"},
    "packages": find_packages("src"),
    "entry_points": {
        "console_scripts": ("{{ cookiecutter.cli_script }} = {{ cookiecutter.app_name }}.cli:main",),
    },
    "data_files": ("etc/",),
}


def main() -> int:
    """ Execute the setup command.

    """
    def data_files(*paths):
        """ Expand path contents for the `data_files` config variable.  """
        for path in map(Path, paths):
            if path.is_dir():
                for root, _, files in walk(str(path)):
                    yield root, tuple(str(Path(root, name)) for name in files)
            else:
                yield str(path.parent), (str(path),)
        return

    def version():
        """ Get the local package version. """
        namespace = {}
        path = Path("src", _config["name"], "__version__.py")
        exec(path.read_text(), namespace)
        return namespace["__version__"]

    _config.update({
        "data_files": list(data_files(*_config["data_files"])),
        "version": version(),
    })
    setup(**_config)
    return 0


# Make the script executable.

if __name__ == "__main__":
    raise SystemExit(main())
