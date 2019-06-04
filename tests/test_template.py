""" Test the Cookiecutter template.

A template project is created in a temporary directory, the application is
installed into a self-contained venv environment, and the application test 
suite is run.

"""
from json import loads
from pathlib import Path
from shlex import split
from shutil import which
from subprocess import check_call
from tempfile import TemporaryDirectory
from venv import create

from cookiecutter.main import cookiecutter


def main() -> int:
    """ Execute the test.
    
    """
    # TODO: Convert to f-strings when Python 3.5 support is dropped.
    template = Path(__file__).resolve().parents[1]
    defaults = loads(template.joinpath("cookiecutter.json").read_text())
    with TemporaryDirectory() as tmpdir:
        cookiecutter(str(template), no_input=True, output_dir=tmpdir)
        cwd = Path(tmpdir) / defaults["project_slug"]
        create(str(cwd / "venv"), with_pip=True)
        bin = str(cwd / "venv" / "bin")  # TODO: Python 3.5 workaround
        pip = which("pip", path=bin) or "pip"  # Travis CI workaround
        install = "{:s} install .".format(pip)
        for req in cwd.glob("**/requirements.txt"):
            install = " ".join((install, "--requirement={!s}".format(req)))
        cwd = str(cwd)  # TODO: Python 3.5 workaround
        check_call(split(install), cwd=cwd)
        pytest = which("pytest", path=bin) or "pytest"  # Travis CI workaround
        check_call(split("{:s} --verbose test".format(pytest)), cwd=cwd)
    return 0
    
    
# Make the script executable.

if __name__ == "__main__":
    raise SystemExit(main())
