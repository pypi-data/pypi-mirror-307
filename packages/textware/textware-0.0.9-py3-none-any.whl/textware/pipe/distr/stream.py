from typing import Iterator, Tuple, TypeAlias

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
    >>> stream = get_pairstream(('Hello world 42 ni hao servus!', 'Lorem ipsum ni hao'))

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
