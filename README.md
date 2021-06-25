# SEAT-CODE Mower Test
**edited at June 25, 2021**

This is the seat-code Mower App (build by [Guillem López Garcia](https://github.com/guiloga)).

## Setup
Project is built with python3, I recommend building it with the latest stable python version: [**python3.9**](https://www.python.org/downloads/release/python-390/).

Create a virtual environment and install all dependencies from **requirements.txt** file:

```bash
# Create the virtual environment
python3.9 -m pip install virtualenv
python3.9 -m virtualenv ~/.virtualenvs/seat-code-test

# Activate and install dependencies
source ~/.virtualenvs/seat-code-test/bin/active
pip install -r requirements.txt
```

## Run Application
Application can be run in two modes: **scheduled** (by a .yaml config file) or **interactive** by command-line input.

### Run in 'scheduled' mode
```bash
# Run with the default config file; --config option can be ommited.
python app.py --config config/app.yml
```

### Run in 'interactive' mode
```bash
# Pass the --interactive flag and the config option will be ommited.
python app.py --interactive
```

## Tests
Tests are buitl with [pytest](https://docs.pytest.org/).

### Run Tests
```bash
python -m pytest
```
### Run Tests with Coverage Report
```bash
python -m pytest --cov=src --cov-report=html
```

> **_NOTE:_** Coverage Report is generated at htmlcov/ folder..
