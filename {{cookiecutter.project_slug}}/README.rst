{% set delim = "#" * cookiecutter.app_name|length -%}
{{ delim }}
{{ cookiecutter.app_name }}
{{ delim }}

Python application created from the `mdklatt/cookiecutter-python-app`_ template.
Python 3.8+ is required.


Development
===========

Create the development environment:

.. code-block:: console

    $ python -m venv .venv
    $ .venv/bin/python -m pip install -e ".[dev]"


Run tests:

.. code-block::

    $ .venv/bin/python -m pytest -v tests/


Build documentation:

.. code-block::

    $ .venv/bin/python -m sphinx -M html docs docs/_build



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



Execution
=========

The installed application includes a wrapper script for command line execution.
The location of this scripts depends on how the application was installed.


Configuration
-------------

The application uses `TOML`_ files for configuration. Configuration supports
runtime parameter substitution via a shell-like variable syntax, *i.e.*
``var = ${VALUE}``. CLI invocation will use the current environment for
parameter substitution, which makes it simple to pass host-specific values
to the application without needing to change the config file for every
installation.

.. code-block:: toml

    mailhost = $SENDMAIL_HOST


Logging
-------

The application uses standard `Python logging`_. All loggins is to ``STDERR``,
nd the logging level can be set via the config file or on the command line.


.. _TOML: https://toml.io
.. _Python logging: https://docs.python.org/3/library/logging.html
.. _mdklatt/cookiecutter-python-app: https://github.com/mdklatt/cookiecutter-python-app