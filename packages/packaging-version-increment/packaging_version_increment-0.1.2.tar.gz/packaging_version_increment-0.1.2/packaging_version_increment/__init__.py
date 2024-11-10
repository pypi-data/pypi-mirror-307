from importlib import metadata as _metadata

from packaging_version_increment.increment import IncrementEnum, increment_version, update_version  # noqa: F401
from packaging_version_increment.version import IncrementVersion  # noqa: F401

try:
    __version__ = _metadata.version('packaging-version-increment')

except _metadata.PackageNotFoundError:  # pragma: no cover
    __version__ = '0.0.0'
