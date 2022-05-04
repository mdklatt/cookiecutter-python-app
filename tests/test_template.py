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
    template = Path(__file__).resolve().parents[1]
    defaults = loads(template.joinpath("cookiecutter.json").read_text())
    with TemporaryDirectory() as tmpdir:
        cookiecutter(str(template), no_input=True, output_dir=tmpdir)
        cwd = Path(tmpdir) / defaults["project_slug"]
        venv = cwd / ".venv"
        create(venv, with_pip=True)
        python = venv / "bin" / "python"
        install = f"{python} -m pip install ."
        for req in cwd.glob("**/requirements.txt"):
            install = " ".join((install, f"--requirement={req}"))
        check_call(split(install), cwd=cwd)
        check_call(split(f"{python} -m pytest --verbose test"), cwd=cwd)
    return 0
    
    
# Make the script executable.

if __name__ == "__main__":
    raise SystemExit(main())
