# winzy-days-till

[![PyPI](https://img.shields.io/pypi/v/winzy-days-till.svg)](https://pypi.org/project/winzy-days-till/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/winzy-days-till?include_prereleases&label=changelog)](https://github.com/sukhbinder/winzy-days-till/releases)
[![Tests](https://github.com/sukhbinder/winzy-days-till/workflows/Test/badge.svg)](https://github.com/sukhbinder/winzy-days-till/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/winzy-days-till/blob/main/LICENSE)

Gives days remaining till the given date

## Installation

First configure your Winzy project [to use Winzy](https://github.com/sukhbinder/winzy).

Then install this plugin in the same environment as your Winzy application.
```bash
pip install winzy-days-till
```
## Usage

To use just type

```bash
winzy days 1 jan 2025
```
This will print out the days.

To make it announce this, use the following command

```bash
winzy days 1 jan 2025 -s "--days-- days remaining to New year!"
```
This will announce the text who you have supplied. `--days--` is a special keyword for days. This will be replaced for no of days remaining. If the `--days--` is not included in the message then a generic announcement is made ignoring user's text.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd winzy-days-till
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
