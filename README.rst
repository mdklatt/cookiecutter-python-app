###################################
Python Application Project Template
###################################

|python3.8|
|python3.9|
|python3.10|
|python3.11|
|license|
|tests|

This is a `Cookiecutter`_ template for creating a Python application project
based on the `Python Packaging User Guide`_.


**Project features:**

- Python 3.8+
- `MIT License`_
- `pytest`_ test suite
- `Sphinx`_ documentation


**Application features:**

- CLI with subcommands
- Standard Python logging
- Hierarchical `TOML`_ configuration


Usage
=====

Install Python requirements for using the template:

.. code-block::

    $ python -m pip install -r requirements.txt


Create a new project directly from the template on `GitHub`_:

.. code-block::

    $ cookiecutter gh:mdklatt/cookiecutter-python-app


Development
===========

Create a local development environment and run template tests:

.. code-block::

    $ make dev test



.. |python3.8| image:: https://img.shields.io/static/v1?label=python&message=3.8&color=informational
   :alt: Python 3.8
.. |python3.9| image:: https://img.shields.io/static/v1?label=python&message=3.9&color=informational
   :alt: Python 3.9
.. |python3.10| image:: https://img.shields.io/static/v1?label=python&message=3.10&color=informational
   :alt: Python 3.10
.. |python3.11| image:: https://img.shields.io/static/v1?label=python&message=3.11&color=informational
   :alt: Python 3.11
.. |license| image:: https://img.shields.io/github/license/mdklatt/httpexec
   :alt: MIT License
   :target: `MIT License`_
.. |tests| image:: https://github.com/mdklatt/cookiecutter-python-app/actions/workflows/test.yml/badge.svg
   :alt: CI Test
   :target: `GitHub Actions`_


.. _Cookiecutter: http://cookiecutter.readthedocs.org
.. _Python Packaging User Guide: https://packaging.python.org/en/latest/tutorials/packaging-projects
.. _GitHub: https://github.com/mdklatt/cookiecutter-python-app
.. _GitHub Actions: https://github.com/mdklatt/cookiecutter-python-app/actions/workflows/test.yml
.. _MIT License: http://choosealicense.com/licenses/mit
.. _pytest: http://pytest.org
.. _Sphinx: http://sphinx-doc.org
.. _TOML: https://toml.io
