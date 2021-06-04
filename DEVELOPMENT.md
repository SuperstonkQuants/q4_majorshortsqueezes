# How to run tests?
Follow the setup in the `README.md` and use the following commands to run all tests:
```
poetry run python -m pytest test/
```

To only run unit tests use the following command:
```
poetry run python -m pytest -m "not integration_test" test/
```

# Dependency management
For the dependency management we use: Conda + Poetry
The initial setup based on the following link.
In order to add or remove dependencies follow these instructions:
https://ealizadeh.com/blog/guide-to-python-env-pkg-dependency-using-conda-poetry#ecd9533df3804417a61b67a70028f4fe
