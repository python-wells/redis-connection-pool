PYMODULES := redisdemo
VENV := .venv
PYTHON := env PYTHONPATH=. $(VENV)/bin/python3
RUFF := $(VENV)/bin/ruff
PYTEST := env PYTEST=1 $(VENV)/bin/pytest
PIP := $(VENV)/bin/python3 -m pip

default: test
venv:
	./utils/ensure_pkg_installed.py python3-pip python3-venv
	if ! test -d $(VENV); then \
		python3 -m venv $(VENV) ; \
	fi
dev-deps: venv
	$(PIP) install -q -r requirements-dev.txt
deps: venv
	$(PIP) install -q -r requirements.txt
lint: deps dev-deps
	$(RUFF) check $(PYMODULES)
	$(RUFF) format $(PYMODULES)
test: lint
	$(PYTEST) $(PYMODULES)
check: test
pipfreeze:
	$(PIP) freeze | tee pip-freeze.txt
shell:
	$(PYTHON) -i -c 'import rss_assist, qb_assist, stats, ptfly'
run:
install:
	$(PIP) install -e .
.PHONY: default venv dev-deps deps check test pipfreeze shell run install
