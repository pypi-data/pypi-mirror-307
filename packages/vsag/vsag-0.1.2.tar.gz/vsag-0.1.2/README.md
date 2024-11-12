# VSAG Python Binding

[![](https://github.com/jiacai2050/vsag-py/actions/workflows/CI.yml/badge.svg)](https://github.com/jiacai2050/vsag-py/actions/workflows/CI.yml)
[![](https://img.shields.io/pypi/v/vsag.svg)](https://pypi.org/project/vsag)

[VSAG](https://github.com/alipay/vsag) is a vector indexing library used for similarity search.

## Installation

```bash
pip install vsag
```

## Development

```
python -m venv .env
source .env/bin/activate
pip install maturin
pip install maturin[patchelf]
```

Useful maturin commands:
```
  build        Build the crate into python packages
  publish      Build and publish the crate as python packages to pypi
  develop      Install the crate as module in the current virtualenv
```
