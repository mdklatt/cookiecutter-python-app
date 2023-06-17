{% set delim = "=" * cookiecutter.app_name|length -%}
{{ delim }}
{{ cookiecutter.app_name }}
{{ delim }}

This is the {{ cookiecutter.app_name }} application.


Minimum Requirements
====================

- Python 3.8+


Optional Requirements
=====================

.. _pytest: http://pytest.org
.. _Sphinx: http://sphinx-doc.org

- `pytest`_ (for running the test suite)
- `Sphinx`_ (for generating documentation)


Basic Setup
===========

Install for the current user:

.. code-block:: console

    $ python -m pip install -e ".[dev]"


Run the application:

.. code-block:: console

    $ python -m {{ cookiecutter.app_name }} --help


Run the test suite:

.. code-block:: console
   
    $ python -m pytest test/


Build documentation:

.. code-block:: console

    $ python -m sphinx -b html doc doc/_build/html
