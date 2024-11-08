r"""Chop text to different kinds of pieces.

- to_lines
- to_sentences
- to_chunks
"""

from typing import List


class PieceMaker:

    @classmethod
    def to_lines(cls, s: str) -> List[str]:
        return s.strip().split('\n')
