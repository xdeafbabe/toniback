.DEFAULT: help
.PHONY: help bootstrap migrate lint test testreport coverage outdated clean

help:
	@echo "Please use '$(MAKE) <target>' where <target> is one of the following:"
	@echo "  help        - show help information"
	@echo "  bootstrap   - initialize virtual environment and install project dependencies"
	@echo "  migrate     - run database migrations"
	@echo "  lint        - inspect project source code for errors"
	@echo "  test        - run project tests"
	@echo "  testreport  - run project tests and open HTML coverage report"
	@echo "  coverage    - run project tests and save coverage to XML file"
	@echo "  outdated    - list outdated project requirements"
	@echo "  clean       - clean up project environment"

VENV = .venv
PYTHON = $(VENV)/bin/python

bootstrap:
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install pip==21.3.1 setuptools==59.1.1 wheel==0.37.0
	$(PYTHON) -m pip install -e .[dev,test,vim]

migrate:
	sudo -u postgres psql -c "CREATE DATABASE toni;"
	sudo -u postgres psql -c "CREATE USER toni WITH ENCRYPTED PASSWORD 'toni';"
	sudo -u postgres psql -c "ALTER USER toni CREATEDB;"
	sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE toni to toni;"
	$(VENV)/bin/alembic upgrade head

lint:
	$(PYTHON) -m flake8 toniback tests

test:
	$(PYTHON) -m pytest --cov-report=term-missing

testreport:
	$(PYTHON) -m pytest --cov-report=html
	xdg-open htmlcov/index.html

coverage:
	$(PYTHON) -m pytest --cov-report=xml

outdated:
	$(PYTHON) -m pip list --outdated --format=columns

clean:
	rm -rf $(VENV) *.egg .eggs *.egg-info .pytest_cache htmlcov .coverage
