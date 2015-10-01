## Test the python-app Cookiecutter template.
##
## A template project is created in a temporary directory, the application is
## installed into a self-contained virtualenv environment, and the application
## test suite is run.
##
set -e  # exit immediately on failure
if [[ "$(uname)" == "Darwin" ]]
then  # OS X uses BSD mktemp
    MKTEMP="mktemp -d -t tmp"
else  # assume Linux/GNU or similar
    MKTEMP="mktemp -d"
fi
template=$(pwd)
project=$(${MKTEMP})
trap "rm -rf $project" EXIT  # remove on exit
pushd $project
cookiecutter $template --no-input
cd pyapp
python setup.py virtualenv
venv/bin/pip install . -r requirements.txt -r requirements-test.txt
venv/bin/py.test --verbose test/
popd
exit 0
