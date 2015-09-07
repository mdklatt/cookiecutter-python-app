Overview
========

This is the {{ cookiecutter.repo_name }} application.


Minimum Requirements
====================

* Python 2.7


Optional Requirements
=====================

* `py.test`_ 2.7 (for running the test suite)
* `Sphinx`_ 1.3 (for generating documentation)


Basic Setup
===========

Run the test suite:

..  code-block::
   
    $ py.test test/

Build documentation:

..  code-block::

    $ cd doc
    $ make html

Install for the current user:

..  code-block::

    $ python setup.py install --user

Run the application:

..  code-block::

    $ python -m {{ cookiecutter.repo_name }}


..  _py.test: http://pytest.org
..  _Sphinx: http://sphinx-doc.org
