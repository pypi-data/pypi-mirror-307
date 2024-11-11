## Packaging
Please refer to:
- https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#package-discovery
- https://packaging.python.org/en/latest/tutorials/packaging-projects/#

## Upload
edit version in pyproject.toml
python3 -m build
python3 -m twine upload --repository testpypi dist/*
python3 -m twine upload dist/*
pip install -U stock_utils_chho33
