{% set delim = "=" * cookiecutter.app_name|length -%}
{{ delim }}
{{ cookiecutter.app_name }}
{{ delim }}

This is the {{ cookiecutter.app_name }} CLI application.


Minimum Requirements
====================

- Python 3.5+


Optional Requirements
=====================

.. _pytest: http://pytest.org
.. _Sphinx: http://sphinx-doc.org

- `pytest`_ (for running the test suite)
- `Sphinx`_ (for generating documentation)


Basic Setup
===========

Install `pre-commit` for linting

.. code-block:: console

    $ pip3 install pre-commit

Install `pre-commit` hooks

.. code-block:: console

    $ pre-commit install

Install this app for the current user:

.. code-block:: console

    $ pip3 install . --user


Run the application:

.. code-block:: console

    $ {{ cookiecutter.app_name }} --help


Run the test suite:

.. code-block:: console

    $ pytest test/


Build documentation:

.. code-block:: console

    $ sphinx-build -b html doc doc/_build/html
