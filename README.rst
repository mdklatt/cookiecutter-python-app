###################################
Python CLI Application Project Template
###################################

|badge|

This is a `Cookiecutter`_ template for creating a Python CLI application project.


================
Project Features
================

- Python 3.7+
- `MIT License`_
- `pytest`_ test suite
- `Sphinx`_ documentation


====================
Application Features
====================

- CLI with subcommands
- Logging
- Hierarchical `YAML`_ configuration


=====
Usage
=====

Install Python requirements for using the template:

.. code-block:: console

  $ pip3 install -r requirements.txt


Create a new project directly from the template on `GitHub`_:

.. code-block:: console

  $ cookiecutter git@github.com:wujiayi101/cookiecutter-python-cli.git


.. _GitHub Actions: https://github.com/mdklatt/cookiecutter-python-app/actions/workflows/test.yml
.. |badge| image:: https://github.com/mdklatt/cookiecutter-python-app/actions/workflows/test.yml/badge.svg
    :alt: GitHub Actions test status
    :target: `GitHub Actions`_
.. _Cookiecutter: http://cookiecutter.readthedocs.org
.. _Python Packaging User Guide: https://packaging.python.org/en/latest/tutorials/packaging-projects
.. _Packaging a Python library: http://blog.ionelmc.ro/2014/05/25/python-packaging
.. _pytest: http://pytest.org
.. _Sphinx: http://sphinx-doc.org
.. _MIT License: http://choosealicense.com/licenses/mit
.. _YAML: http://pyyaml.org/wiki/PyYAML
.. _GitHub: https://github.com/mdklatt/cookiecutter-python-app
