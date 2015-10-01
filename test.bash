## Test the python-app Cookiecutter template.
##
## This verifies that a sample project can be created from the template, be
## installed, and pass a basic test suite.
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
echo $template
echo $project
cookiecutter $template --no-input
cd pyapp
python setup.py virtualenv -r requirements-test.txt
venv/bin/pip install .
venv/bin/py.test --verbose test/
popd
exit 0
