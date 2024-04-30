# alliance-genotype

KGX transform of Alliance affected_genomic_model and associations to genotype components

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)

## Requirements

- Python >= 3.10
- [Poetry](https://python-poetry.org/docs/#installation)

## Installation

```bash
cd alliance-genotype
make install
# or
poetry install
```

> **Note** that the `make install` command is a convenience wrapper around `poetry install`.

Once installed, you can check that everything is working as expected:

```bash
# Run the pytest suite
make test
# Download the data and run the Koza transform
make download
make run
```

## Usage

This project is set up with a Makefile for common tasks.  
To see available options:

```bash
make help
```

### Download and Transform

To download the data for the alliance_genotype transform:

```bash
poetry run ingest download
```

To run the Koza transform for alliance-genotype:

```bash
poetry run ingest transform
```

To see available options:

```bash
poetry run ingest download --help
# or
poetry run ingest transform --help
```

---

> This project was generated using [monarch-initiative/cookiecutter-monarch-ingest](https://github.com/monarch-initiative/cookiecutter-monarch-ingest).  
> Keep this project up to date using cruft by occasionally running in the project directory:
>
> ```bash
> cruft update
> ```
>
> For more information, see the [cruft documentation](https://cruft.github.io/cruft/#updating-a-project)
