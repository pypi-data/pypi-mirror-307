from typing import Any, Optional

from packaging.version import Version

from packaging_version_increment.enums import IncrementEnum


def update_version(
    version: Version,
    major: int = 0,
    minor: int = 0,
    micro: int = 0,
    a: Optional[int] = None,
    b: Optional[int] = None,
    c: Optional[int] = None,
    rc: Optional[int] = None,
    alpha: Optional[int] = None,
    beta: Optional[int] = None,
    pre: Optional[int] = None,
    preview: Optional[int] = None,
    post: Optional[int] = None,
    rev: Optional[int] = None,
    r: Optional[int] = None,
    dev: Optional[int] = None,
    local: Optional[Any] = None,
):
    pre_number, pre_name = next(
        (
            (n, name)
            for n, name in zip(
                [a, b, c, rc, alpha, beta, pre, preview],
                ['a', 'b', 'c', 'rc', 'alpha', 'beta', 'pre', 'preview'],
            )
            if n is not None
        ),
        (0, None),
    )

    post_number, post_name = next(
        (
            (n, name)
            for n, name in zip(
                [post, rev, r],
                ['post', 'rev', 'r'],
            )
            if n is not None
        ),
        (0, None),
    )

    new_major = version.major + major
    new_minor = version.minor + minor
    new_micro = version.micro + micro

    if version.pre is not None:
        pre_number += version.pre[1]
        pre_name = pre_name or version.pre[0]

    if version.post is not None:
        post_number += version.post
        post_name = post_name or 'post'

    if dev is not None and version.dev is not None:
        dev += version.dev

    if pre_number and version.pre is None:
        new_micro += 1

    version_str = f'{new_major}.{new_minor}.{new_micro}'

    if pre_number:
        version_str += f'{pre_name}{pre_number}'

    if post_number:
        version_str += f'.{post_name}{post_number}'

    if dev is not None:
        version_str += f'.dev{dev}'

    if local is not None:
        version_str += f'+{local}'

    return Version(version_str)


def increment_version(version: Version, part: IncrementEnum) -> Version:  # noqa: C901
    if part == IncrementEnum.major:
        return update_version(
            version,
            major=1,
            minor=-version.minor,
            micro=-version.micro,
            pre=-version.pre[1] if version.pre is not None else 0,
            post=-version.post if version.post is not None else 0,
        )
    if part == IncrementEnum.minor:
        return update_version(
            version,
            minor=1,
            micro=-version.micro,
            pre=-version.pre[1] if version.pre is not None else 0,
            post=-version.post if version.post is not None else 0,
        )
    if part == IncrementEnum.micro:
        return update_version(
            version,
            micro=1,
            pre=-version.pre[1] if version.pre is not None else 0,
            post=-version.post if version.post is not None else 0,
        )
    if part == IncrementEnum.a:
        return update_version(version, a=1)
    if part == IncrementEnum.b:
        return update_version(version, b=1)
    if part == IncrementEnum.c:
        return update_version(version, c=1)
    if part == IncrementEnum.rc:
        return update_version(version, rc=1)
    if part == IncrementEnum.alpha:
        return update_version(version, alpha=1)
    if part == IncrementEnum.beta:
        return update_version(version, beta=1)
    if part == IncrementEnum.pre:
        return update_version(version, pre=1)
    if part == IncrementEnum.preview:
        return update_version(version, preview=1)
    if part == IncrementEnum.post:
        return update_version(version, post=1)
    if part == IncrementEnum.rev:
        return update_version(version, rev=1)
    if part == IncrementEnum.r:
        return update_version(version, r=1)
    if part == IncrementEnum.dev:
        return update_version(version, dev=1)
    if part == IncrementEnum.local:
        return update_version(version, local=1)
