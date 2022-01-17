# Wordle Assistant

Tools to remove all the fun from playing Wordle

## Installation

You should create a virtual environment first with your preferred tool.

Then install the project with [poetry](https://python-poetry.org/):

```bash
poetry install
```

## Usage

```bash
python src/stats.py --dictionary-path data/dictionary_fr.txt --word-length 8
```

## Contributing

### Dependencies

Adding dependencies to the project can be done with a simple:

```bash
poetry add <package-name>
```

### Formatting

Always run `black` and `isort` on all the code of the package (including the example project):

```bash
black src
isort src
```

### Additional linter

Even though `black` does a great job a formatting the code, some lint warnings can sneak through it, so
we also use `flake8` (with a custom configuration):

```bash
flake8 src
```

### Type hinting

To check the type hinting is correct, simply run:

```bash
mypy --pretty src
```
