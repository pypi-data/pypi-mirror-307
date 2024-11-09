from typing import Iterator, TypeAlias

from textware.core.counting.counter import CoolCounter
from textware.core.transprocessing.base_processor import Transcessor

DocStream: TypeAlias = Iterator[str]


def distr_unistate(
    docs: DocStream
) -> CoolCounter:
    """A pipe to count the word frequency

    A markov chain with just one state

    Parameters
    ----------
    docs : Stream

    Examples
    --------
    >>> cnt = freq_pipe(docs=['foo BAR ', 'Hello foo world!'])
    >>> cnt.counts
    Counter({'foo': 2, 'bar': 1, 'hello': 1, 'world': 1, '!': 1})

    Returns
    -------
    CoolCounter
    """

    cnt = CoolCounter(
        Transcessor.flatten_words(Transcessor.render(docs))
    )
    return cnt
