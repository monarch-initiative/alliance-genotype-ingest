ROOTDIR = $(shell pwd)
RUN = poetry run
VERSION = $(shell poetry -C src/alliance_genotype version -s)

### Help ###

define HELP
╭───────────────────────────────────────────────────────────╮
  Makefile for alliance_genotype			    
│ ───────────────────────────────────────────────────────── │
│ Usage:                                                    │
│     make <target>                                         │
│                                                           │
│ Targets:                                                  │
│     help                Print this help message           │
│                                                           │
│     all                 Install everything and test       │
│     fresh               Clean and install everything      │
│     clean               Clean up build artifacts          │
│     clobber             Clean up generated files          │
│                                                           │
│     install             Poetry install package            │
│     download            Download data                     │
│     run                 Run the transform                 │
│                                                           │
│     docs                Generate documentation            │
│                                                           │
│     test                Run all tests                     │
│                                                           │
│     lint                Lint all code                     │
│     format              Format all code                   │
╰───────────────────────────────────────────────────────────╯
endef
export HELP

.PHONY: help
help:
	@printf "$${HELP}"


### Installation and Setup ###

.PHONY: fresh
fresh: clean clobber all

.PHONY: all
all: install test

.PHONY: install
install: 
	poetry install


### Documentation ###

.PHONY: docs
docs:
	$(RUN) mkdocs build


### Testing ###

.PHONY: test
test: download
	$(RUN) pytest tests


### Running ###

.PHONY: download
download:
	$(RUN) ingest download

data/allele-to-gene-map.tsv: download
	$(RUN) python scripts/generate-allele-to-gene-map.py

.PHONY: run
run: download data/allele-to-gene-map.tsv
	$(RUN) ingest transform
	$(RUN) python scripts/generate-report.py


### Linting, Formatting, and Cleaning ###

.PHONY: clean
clean:
	rm -f `find . -type f -name '*.py[co]' `
	rm -rf `find . -name __pycache__` \
		.venv .ruff_cache .pytest_cache **/.ipynb_checkpoints

.PHONY: clobber
clobber:
	# Add any files to remove here
	@echo "Nothing to remove. Add files to remove to clobber target."

.PHONY: lint
lint: 
	$(RUN) ruff check --diff --exit-zero
	$(RUN) black -l 120 --check --diff src tests

.PHONY: format
format: 
	$(RUN) ruff check --fix --exit-zero
	$(RUN) black -l 120 src tests
