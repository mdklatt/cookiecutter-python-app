Python Application Project Template
===================================

Overview |travis.png|
---------------------
..  _travis: https://travis-ci.org/mdklatt/cookiecutter-python-app
..  _Cookiecutter: http://cookiecutter.readthedocs.org
..  _packaging guidelines: https://packaging.python.org/en/latest/distributing.html#configuring-your-project
..  _Packaging a Python library: http://blog.ionelmc.ro/2014/05/25/python-packaging/


This is a `Cookiecutter`_ template for creating a Python application project.

This template departs from the current Python `packaging guidelines`_ that
discourage the use of a source directory, but moving the package out of the
project root provides several advantages (*cf.* `Packaging a Python library`_).

..  |travis.png| image:: https://travis-ci.org/mdklatt/cookiecutter-python-app.png?branch=master
    :alt: Travis CI build status
    :target: `travis`_


Template Project Features
-------------------------
..  _pytest: http://pytest.org
..  _Sphinx: http://sphinx-doc.org
..  _MIT License: http://choosealicense.com/licenses/mit
..  _Virtualenv: https://virtualenv.pypa.io


* Python 2.7
* `MIT License`_
* `pytest`_ tests
* `Sphinx`_ documentation
* `Virtualenv`_ deployment



Template Application Features
-----------------------------
..  _YAML: http://pyyaml.org/wiki/PyYAML


* CLI with subcommands
* Logging
* Hierarchical `YAML`_ configuration


Usage
-----
..  _GitHub: https://github.com/mdklatt/cookiecutter-python-app


Install Python requirements for using the template:

..  code-block::

    $ pip install --requirement=requirements.txt --user 


Create a new project directly from the template on `GitHub`_:

..  code-block::
   
    $ cookiecutter gh:mdklatt/cookiecutter-python-app
