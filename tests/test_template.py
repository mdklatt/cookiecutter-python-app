""" Test the Cookiecutter template.

A template project is created in a temporary directory, the application is
installed into a self-contained venv environment, and the application test 
suite is run.

"""
from cookiecutter.generate import generate_context
from cookiecutter.main import cookiecutter
from pathlib import Path
from shlex import split
from subprocess import run
from venv import create

import pytest


@pytest.fixture(scope="session")
def template() -> Path:
    """ The template under test.

    """
    return Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def tmpdir(tmp_path_factory) -> Path:
    """ Test directory.

    """
    return tmp_path_factory.mktemp("test_template")


@pytest.fixture(scope="module")
def context(template) -> dict:
    """ Template context for testing.

    """
    context = generate_context(template.joinpath("cookiecutter.json"))
    context["cookiecutter"].update({
        "app_name": context["cookiecutter"]["project_slug"],
        "author_name": "J. Smith",
        "author_email": "jsmith@example.com",
        "project_url": "http://project.example.com",
    })
    return context["cookiecutter"]


@pytest.fixture(scope="module")
def project(tmpdir, template, context) -> Path:
    """ Create a test project from the Cookiecutter template.

    """
    cookiecutter(str(template), no_input=True, output_dir=tmpdir, extra_context=context)
    return tmpdir / context["project_slug"]


@pytest.fixture
def python(tmp_path):
    """ Create a Python virtual environment for testing.

    """
    venv = tmp_path / ".venv"
    create(venv, with_pip=True)
    return venv / "bin" / "python"


def test_project(project):
    """ Verify that the project was created correctly.

    """
    # Just a basic sanity test.
    assert len(list(project.iterdir())) == 8
    return


def test_dev(project, python):
    """ Test the creation of the project dev environment.

    """
    install = f"pip install -e .[dev]"
    test = "pytest tests/"
    for command in install, test:
        args = split(f"{python} -m {command}")
        process = run(args, cwd=project)
        assert process.returncode == 0
    return


def test_app(context, project, python):
    """ Test the installed application.

    """
    install = f"pip install {project}"
    cli = f"{context['app_name']}.cli --help"
    for command in install, cli:
        args = split(f"{python} -m {command}")
        process = run(args)
        assert process.returncode == 0
    return


# Make the script executable.

if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
