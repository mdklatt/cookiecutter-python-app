# Project management tasks.

VENV = .venv
PYTHON = source $(VENV)/bin/activate && python


$(VENV)/.make-update: requirements.txt
	python -m venv $(VENV)
	$(PYTHON) -m pip install -r $^
	touch $@


.PHONY: dev
dev: $(VENV)/.make-update


.PHONY: test
test: dev
	@$(PYTHON) tests/test_template.py && echo "All tests passed"
