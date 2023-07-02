# Project management tasks.

VENV = .venv
PYTHON = . $(VENV)/bin/activate && python
PYTEST = $(PYTHON) -m pytest


$(VENV)/.make-update: pyproject.toml
	python -m venv $(VENV)
	$(PYTHON) -m pip install -U pip  # needs to be updated first
	$(PYTHON) -m pip install -e ".[dev]"
	touch $@


.PHONY: dev
dev: $(VENV)/.make-update


.PHONY: docs
docs: dev
	$(PYTHON) -m sphinx -M html docs docs/_build


.PHONY: test-unit
test-unit: dev
	$(PYTEST) tests/unit/


.PHONY: check
check: test-unit
