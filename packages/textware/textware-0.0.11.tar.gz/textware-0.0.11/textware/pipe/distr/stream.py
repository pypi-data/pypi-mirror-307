import random
from itertools import permutations
from typing import Dict, Iterator, Tuple, TypeAlias

from textware.core import BatchMaker, Transcessor

DocStream: TypeAlias = Iterator[str]


def get_pairstream(
    docs: DocStream,
    batchsize: int = 5
) -> Iterator[Tuple[str, str]]:
    """Create a stream of pairs

    Parameters
    ----------
    docs : DocStream
    batchsize : int, optional
        Size of the LearningWindow, by default 5

    Examples
    --------
    >>> stream = get_pairstream(('Hello world 42 ni hao servus!', 'Lorem ipsum ni hao'), batchsize=3)
    >>> pairs = list(stream)
    >>> pairs[0:4]
    [('hello', 'world'), ('hello', 'ni'), ('world', 'ni'), ('world', 'hao')]

    Returns
    -------
    Iterator[Tuple[str, str]]:
        A stream of pairs
    """

    doctokens = Transcessor.get_words_from_docs(
        docs,
        filters=[Transcessor.remove_pure_nums]
    )
    for batch in BatchMaker.get_batches(doctokens, batchsize=batchsize):
        for prio in batch[0:-1]:
            yield (prio, batch[-1])


def get_pairstream_with_prior(
    docs: DocStream,
    bay: Dict[str, Dict[str, float]],
    batchsize: int = 5
) -> Iterator[Tuple[Tuple[str, str], str]]:
    """Create a stream of pairs

    Parameters
    ----------
    docs : DocStream
    batchsize : int, optional
        Size of the LearningWindow, by default 5

    Examples
    --------
    >>> stream = get_pairstream_with_prior(('Hello world 42 ni hao servus! Lorem ipsum ni hao', ), bay={'ni': {'hao': 10}, 'hao': {'world': 2}}, batchsize=3)
    >>> list(stream)
    [(('ni', 'hao'), 'servus'), (('ni', 'hao'), 'lorem')]

    Returns
    -------
    Iterator[Tuple[str, str]]:
        A stream of pairs where first item is a path-key
    """

    doctokens = Transcessor.get_words_from_docs(
        docs,
        filters=[Transcessor.remove_pure_nums]
    )
    for batch1, batch2 in BatchMaker.get_cobatches(docs=doctokens, batchsize=batchsize, offset=batchsize):
        # Pick some from the anchor
        samplesize = 10
        context = {w for w in batch1 if w in bay}
        n = len(context)
        if not n >= 2 or not batch2:
            continue
        size = min(samplesize, n * (n - 1))
        for w, u in random.sample(list(permutations(context, 2)), size):
            if u in bay[w]:
                v = batch2[0]
                yield ((w, u), v)
