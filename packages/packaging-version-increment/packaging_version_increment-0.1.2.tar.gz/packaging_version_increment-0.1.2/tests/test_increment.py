import pytest
from packaging.version import Version

from packaging_version_increment import IncrementEnum, increment_version


@pytest.mark.parametrize(
    'version, part, result',
    [
        ('0.0.0', IncrementEnum.major, '1.0.0'),
        ('0.0.0', IncrementEnum.minor, '0.1.0'),
        ('0.0.0', IncrementEnum.micro, '0.0.1'),
        #
        ('1.1.1', IncrementEnum.major, '2.0.0'),
        ('1.1.1', IncrementEnum.minor, '1.2.0'),
        ('1.1.1', IncrementEnum.micro, '1.1.2'),
        #
        ('0.0.1a1', IncrementEnum.major, '1.0.0'),
        ('0.0.1a1', IncrementEnum.minor, '0.1.0'),
        ('0.0.1a1', IncrementEnum.micro, '0.0.2'),
        #
        ('0.0.0', IncrementEnum.a, '0.0.1a1'),
        ('0.0.0', IncrementEnum.alpha, '0.0.1a1'),
        ('0.0.0', IncrementEnum.b, '0.0.1b1'),
        ('0.0.0', IncrementEnum.beta, '0.0.1b1'),
        ('0.0.0', IncrementEnum.c, '0.0.1rc1'),
        ('0.0.0', IncrementEnum.rc, '0.0.1rc1'),
        ('0.0.0', IncrementEnum.pre, '0.0.1rc1'),
        ('0.0.0', IncrementEnum.preview, '0.0.1rc1'),
        ('0.0.0', IncrementEnum.post, '0.0.0.post1'),
        ('0.0.0', IncrementEnum.rev, '0.0.0.post1'),
        ('0.0.0', IncrementEnum.r, '0.0.0.post1'),
        ('0.0.0', IncrementEnum.dev, '0.0.0.dev1'),
        #
        ('0.0.1a1', IncrementEnum.post, '0.0.1a1.post1'),
        ('0.0.1a1', IncrementEnum.dev, '0.0.1a1.dev1'),
        #
        ('0.0.1a1.post1', IncrementEnum.post, '0.0.1a1.post2'),
        ('0.0.1a1.post1.dev1', IncrementEnum.dev, '0.0.1a1.post1.dev2'),
    ],
)
def test_increment_version(version: str, part: IncrementEnum, result: str):
    new_version = increment_version(Version(version), part)
    assert str(new_version) == result
