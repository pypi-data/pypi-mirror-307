import pytest
from packaging.version import Version

from packaging_version_increment import IncrementEnum, increment_version


@pytest.mark.parametrize(
    'version, part, result',
    [
        ('0.0.0', IncrementEnum.major, '1.0.0'),
        ('0.0.0', IncrementEnum.minor, '0.1.0'),
        ('0.0.0', IncrementEnum.patch, '0.0.1'),
        ('0.0.0', IncrementEnum.prerelease, '0.0.1a1'),
        ('0.0.1a1', IncrementEnum.prerelease, '0.0.1a2'),
        ('0.0.1a1', IncrementEnum.major, '1.0.0'),
        ('0.0.1a1', IncrementEnum.minor, '0.1.0'),
        ('0.0.1a1', IncrementEnum.patch, '0.0.2'),
    ],
)
def test_increment_version(version: str, part: IncrementEnum, result: str):
    new_version = increment_version(Version(version), part)
    assert str(new_version) == result
