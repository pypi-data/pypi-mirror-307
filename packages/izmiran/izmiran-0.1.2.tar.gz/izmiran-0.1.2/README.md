# Project Name

## Description

IZMIRAN library for common tasks.

## Documents

No additional documents are provided.

## Software Requirements

* Python 3.7+
* make

## Dependencies

* pytest
* yapf
* bandit

## Usage and installation

```bash
$ pip install izmiran
```

***API is liquid due to development process. Use exact versioning!***

## Developing Process

* Used feature-flow for developing

## Release Process

### Release Process - Step 1 - Verify and validate codebase

Run:

```bash
make all_release
```

### Release Process - Step 2 - Update version

Go to [pyproject.toml](./pyproject.toml) and [setup.py](./setup.py) and update `version`.


### Release Process - Step 3 - Update CHANGELOG.md

Go to [CHANGELOG.md](./CHANGELOG.md) and update it.

### Release Process - Step 4 - Check installation of target

```bash
$ make install
```

### Release Process - Step 5 - Update package on PyPI

```bash
make publish
```
