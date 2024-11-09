# sec_yf

A package for downloading accounting and market data from SEC regulated companies.

## Installation

```bash
$ pip install sec_yf
```

## Usage

Prepare and download all data from a universe of companies:

```python
from sec_yf.download_sec import download_and_prepare_data
from sec_yf.yahoo_finance import get_all_data

# Download and prepare data from SEC
download_and_prepare_data()

# Get all data from Yahoo Finance
get_all_data()
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`sec_yf` was created by Juan F. Imbet. It is licensed under the terms of the MIT license.

## Credits

`sec_yf` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
