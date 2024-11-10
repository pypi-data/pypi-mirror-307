from enum import Enum


class IncrementEnum(str, Enum):
    major = 'major'
    minor = 'minor'
    micro = 'micro'
    a = 'a'
    b = 'b'
    c = 'c'
    rc = 'rc'
    alpha = 'alpha'
    beta = 'beta'
    pre = 'pre'
    preview = 'preview'
    post = 'post'
    rev = 'rev'
    r = 'r'
    dev = 'dev'
    local = 'local'
