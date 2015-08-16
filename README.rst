Python Application Project Template
===================================

Overview
--------

This is a `Cookiecutter`_ template for creating a Python application project.

This template departs from the current Python `packaging guidelines`_ that
discourage the use of a *src* directory, but moving the package out of the
project root provides several advantages (*cf.* `Packaging a python library`_).


Template Project Features
-------------------------

* `py.test`_ tests
* `Sphinx`_ documentation
* `MIT license`_
* Custom setup.py command for creating `virtualenv`_ environments


Minimum Requirements
--------------------

* Python 2.7
* `Cookiecutter`_ 1.0


Usage
-----

Create a new project directly from the template on `GitHub`_:

..  code-block::
   
    $ cookiecutter gh:mdklatt/cookiecutter-python-app.git


..  _Cookiecutter: http://cookiecutter.readthedocs.org
..  _packaging guidelines: https://packaging.python.org/en/latest/distributing.html#configuring-your-project
..  _Packaging a python library: http://blog.ionelmc.ro/2014/05/25/python-packaging/
..  _py.test: http://pytest.org
..  _Sphinx: http://sphinx-doc.org
..  _MIT license: http://choosealicense.com/licenses/mit
..  _virtualenv: https://virtualenv.pypa.io
..  _GitHub: https://github.com/mdklatt/cookiecutter-python-app
