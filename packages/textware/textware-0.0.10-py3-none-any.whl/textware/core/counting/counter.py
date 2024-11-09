"""Wrap around the standard counter
"""


from collections import Counter, defaultdict
from typing import Any, Dict, Iterable, Tuple

import numpy as np


class CoolCounter:
    """Wrap around the standard counter

    samplesize: int
        number of samples where within each sample the items are counted
    """

    def __init__(self, items=None) -> None:
        self.counts: Counter = Counter()
        self.samplesize: int = 0
        if items is not None:
            self.count(items)

    def __call__(self, stream: Iterable) -> Any:
        self.counts = Counter(stream)

    def __getitem__(self, key: str) -> int:
        return self.counts.get(key, 0)

    def __len__(self):
        return len(self.counts)

    def reset(self):
        self.counts = Counter()
        self.samplesize = 0

    @property
    def size(self) -> int:
        return len(self.counts)

    def topn(self, n=10):
        return self.counts.most_common(n=n)

    def count(
        self,
        iterable: Iterable[str]
    ):
        self.counts.update(iterable)
        self.samplesize += 1

    def chaincount(
        self,
        iterables: Iterable[Iterable[str]]
    ):
        for inner in iterables:
            self.count(inner)

    def chaincount_unique(
        self,
        iterables: Iterable[Iterable[str]]
    ):
        """_summary_

        Parameters
        ----------
        iterables : Iterable[Iterable[str]]
            _description_

        Example
        -------
        >>> cnter = CoolCounter()
        >>> cnter.chaincount_unique(['abc', 'ab', 'aaaaaa'])
        >>> cnter.counts['a']
        3
        """
        for inner in iterables:
            self.count(set(inner))

    @classmethod
    def merge(
        cls,
        counters: Iterable[Counter]
    ) -> Counter:
        cnt = Counter()
        for counter in counters:
            cnt.update(counter)
        return cnt

    @property
    def total(self) -> int:
        return sum(self.counts.values())

    @property
    def frequencies_as_arrays(
        self
    ) -> Tuple[np.ndarray, np.ndarray]:
        total = self.total
        counts = self.counts
        keys = np.array(list(counts.keys()))
        freqs = np.array(
            [count / total for count in counts.values()], dtype=float)
        return keys, freqs

    @property
    def frequencies(
        self
    ) -> Dict[str, float]:
        total = self.total
        freqs = {
            name: count / total
            for name, count in self.counts.items()
        }
        return freqs


if __name__ == "__main__":
    import doctest
    doctest.testmod()
