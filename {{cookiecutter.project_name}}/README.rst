{{ "=" * cookiecutter.app_name|length }}
{{ cookiecutter.app_name }}
{{ "=" * cookiecutter.app_name|length }}


This is the {{ cookiecutter.app_name }} application.


Minimum Requirements
====================

- Python 2.7


Optional Requirements
=====================
..  _pytest: http://pytest.org
..  _Sphinx: http://sphinx-doc.org

- `pytest`_ (for running the test suite)
- `Sphinx`_ (for generating documentation)


Basic Setup
===========

Install for the current user:

..  code-block:: console

    $ python setup.py install --user


Run the application:

..  code-block:: console

    $ python -m {{ cookiecutter.app_name }} --help


Run the test suite:

..  code-block:: console
   
    $ pytest test/


Build documentation:

..  code-block:: console

    $ cd doc && make html
    
    
Deploy the application in a self-contained `Virtualenv`_ environment:

..  _Virtualenv: https://virtualenv.readthedocs.org

..  code-block:: console

    $ python deploy.py /path/to/apps
    $ cd /path/to/apps/{{ cookiecutter.app_name }} && bin/cli --help
