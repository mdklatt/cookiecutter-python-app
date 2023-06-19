{% set delim = "#" * cookiecutter.app_name|length -%}
{{ delim }}
{{ cookiecutter.app_name }}
{{ delim }}

This is the {{ cookiecutter.app_name }} application. Python 3.8+ is required.


Development
===========

Create the development environment:

.. code-block:: console

    $ python -m venv .venv
    $ .venv/bin/python -m pip install -e ".[dev]"


Run tests:

.. code-block::

    $ .venv/bin/python -m pytest -v test/


Run the test suite:

.. code-block::
   
    $ .venv/bin/python -m pytest test/


Build documentation:

.. code-block::

    $ .venv/bin/python -m sphinx -b html doc doc/_build/html



Installation
============

Packaging and distributing a Python application is dependent on the target
operating system(s) and execution environment, which could be a Python virtual
environment, Linux container, or native application.

Install the application to a self-contained Python virtual environment:

    $ python -m venv .venv
    $ .venv/bin/python -m pip install <project source>
    $ cp -r <project source>/etc .venv/
    $ .venv/bin/{{ cookiecutter.cli_script }} --help
