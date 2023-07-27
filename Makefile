NAME := app
INSTALL_STAMP := .install.stamp
POETRY := $(shell command -v poetry 2> /dev/null)

.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo ""
	@echo "  install     install packages and prepare environment"
	@echo "  clean       remove all temporary files"
	@echo "  lint        run the code linters"
	@echo "  format      reformat code"
	@echo "  test        run all the tests"
	@echo ""
	@echo "Check the Makefile to know exactly what each target is doing."

install: $(INSTALL_STAMP)
$(INSTALL_STAMP): pyproject.toml poetry.lock
	@if [ -z $(POETRY) ]; then echo "Poetry could not be found. See https://python-poetry.org/docs/"; exit 2; fi
	$(POETRY) install
	touch $(INSTALL_STAMP)

.PHONY: clean
clean:
	find . -type d -name "__pycache__" | xargs rm -rf {};
	rm -rf $(INSTALL_STAMP) .coverage .mypy_cache

.PHONY: lint
lint: $(INSTALL_STAMP)
	$(POETRY) run isort $(NAME) --check-only
	$(POETRY) run black $(NAME) --diff
	$(POETRY) run flake8 $(NAME)
	$(POETRY) run mypy $(NAME)
	$(POETRY) run bandit -r $(NAME)

.PHONY: format
format: $(INSTALL_STAMP)
	$(POETRY) run isort $(NAME)
	$(POETRY) run black $(NAME)

.PHONY: test
test: $(INSTALL_STAMP)
	$(POETRY) run pytest tests -vvv

.PHONY: dbscripts
dbscripts: $(INSTALL_STAMP)
	$(POETRY) run python $(NAME)/generate_db_scripts.py

.PHONY: watch
watch: $(INSTALL_STAMP)
	$(POETRY) run uvicorn $(NAME).main:rest --reload