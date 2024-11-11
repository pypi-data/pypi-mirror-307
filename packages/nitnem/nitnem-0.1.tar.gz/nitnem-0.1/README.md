# nitnem

[![PyPI](https://img.shields.io/pypi/v/nitnem.svg)](https://pypi.org/project/nitnem/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/nitnem?include_prereleases&label=changelog)](https://github.com/sukhbinder/nitnem/releases)
[![Tests](https://github.com/sukhbinder/nitnem/actions/workflows/test.yml/badge.svg)](https://github.com/sukhbinder/nitnem/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/nitnem/blob/master/LICENSE)

Nitnem using python for Mac and possibly windows latter

## Installation

Install this tool using `pip`:
```bash
pip install nitnem
```
## Usage

For help, run:
```bash
nitnem --help
```
You can also use:
```bash
python -m nitnem --help
```
## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd nitnem
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
