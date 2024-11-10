# packaging-version-increment

Implementation of version increase following PEP 440 and SemVer conventions

[![PyPI](https://img.shields.io/pypi/v/packaging-version-increment)](https://pypi.org/project/packaging-version-increment/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/packaging-version-increment)](https://pypi.org/project/packaging-version-increment/)

[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=rocshers_packaging-version-increment&metric=coverage)](https://sonarcloud.io/summary/new_code?id=rocshers_packaging-version-increment)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=rocshers_packaging-version-increment&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=rocshers_packaging-version-increment)

[![Downloads](https://static.pepy.tech/badge/packaging-version-increment)](https://pepy.tech/project/packaging-version-increment)
[![GitLab stars](https://img.shields.io/gitlab/stars/rocshers/python/packaging-version-increment)](https://gitlab.com/rocshers/python/packaging-version-increment)
[![GitLab last commit](https://img.shields.io/gitlab/last-commit/rocshers/python/packaging-version-increment)](https://gitlab.com/rocshers/python/packaging-version-increment)

## Documentation

Install:

```bash
pip install packaging-version-increment
```

Usage:

```python
from packaging.version import Version
from packaging_version_increment import increment_version, IncrementEnum

version = Version('0.0.0')
print(version) # 0.0.0

new_version = increment_version(version, IncrementEnum.major)
print(new_version) # 1.0.0
```

## Contribute

Issue Tracker: <https://gitlab.com/rocshers/python/packaging-version-increment/-/issues>  
Source Code: <https://gitlab.com/rocshers/python/packaging-version-increment>

Before adding changes:

```bash
make install
```

After changes:

```bash
make format test
```
