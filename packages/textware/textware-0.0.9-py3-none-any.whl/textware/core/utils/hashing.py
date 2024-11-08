import hashlib
from typing import Iterable


def hash_id(s: str, size: int = 16) -> str:
    return hashlib.md5(s.lower().encode("utf-8")).hexdigest()[0:size]


def hash_iter(*seq: Iterable[str], size: int = 16) -> str:
    return hash_id(''.join(seq), size=size)
