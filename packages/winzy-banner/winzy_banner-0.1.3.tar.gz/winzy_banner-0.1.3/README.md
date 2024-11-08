# winzy-banner

[![PyPI](https://img.shields.io/pypi/v/winzy-banner.svg)](https://pypi.org/project/winzy-banner/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/winzy-banner?include_prereleases&label=changelog)](https://github.com/sukhbinder/winzy-banner/releases)
[![Tests](https://github.com/sukhbinder/winzy-banner/workflows/Test/badge.svg)](https://github.com/sukhbinder/winzy-banner/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/winzy-banner/blob/main/LICENSE)

Display Banner text

## Installation

First configure your Winzy project [to use Winzy](https://github.com/sukhbinder/winzy).

Then install this plugin in the same environment as your Winzy application.
```bash
pip install winzy-banner
```
## Usage

Type this

```bash
winzy banner Display Your Text Here
```

It will display

![winzy banner](banner.png)

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd winzy-banner
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
