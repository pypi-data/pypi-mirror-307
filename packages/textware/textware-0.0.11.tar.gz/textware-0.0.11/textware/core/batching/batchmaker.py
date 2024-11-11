
from __future__ import annotations

from collections.abc import Iterable
from itertools import islice
from typing import Literal, Tuple, Union


class BatchMaker:
    """Create batches
    """

    @classmethod
    def get_doc_batches(
        cls,
        docs: Iterable[str],
        batchsize: int = 1000  # Normally a large number
    ) -> Iterable[Iterable[str]]:
        """Return batches of N-docs

        Parameters
        ----------
        docs : Iterable[str]
            _description_
        batchsize : int, optional
            _description_, by default 1000#Normallyalargenumber

        Examples
        --------
        >>> docbatches = BatchMaker.get_doc_batches(docs=('hey', 'world', 'ab cd', 'x!'), batchsize=2)
        >>> list(docbatches)
        [['hey', 'world'], ['ab cd', 'x!']]

        Yields
        ------
        Iterator[Iterable[str]]
            _description_
        """
        it = iter(docs)  # Use `iterator` to exhaust it
        while True:
            batch = list(islice(it, batchsize))
            if not batch:
                break
            yield batch

    @classmethod
    def get_batches(
        cls,
        docs: Iterable[Iterable[str]],
        batchsize: int
    ) -> Iterable[Iterable[str]]:
        """Get batches from a docstream

        NOTE:
        * it slides in and slides out, with a min batchsize = 2

        Parameters
        ----------
        docs : Iterable[Iterable[str]]
            The `Doc Stream`
        batchsize : int

        Example
        -------
        >>> docs = ['abce', 'CD E F']
        >>> batches = BatchMaker.get_batches(docs, batchsize=3)
        >>> bchs = list(batches)
        >>> bchs[0: 4]
        [['a', 'b'], ['a', 'b', 'c'], ['b', 'c', 'e'], ['C', 'D']]
        >>> bchs[-1:]
        [['E', ' ', 'F']]
        >>> docs = ['xy']
        >>> batches = BatchMaker.get_batches(docs, batchsize=3)
        >>> bchs = list(batches)
        >>> bchs
        [['x', 'y']]
        >>> docs = ['B']
        >>> batches = BatchMaker.get_batches(docs, batchsize=3)
        >>> bchs = list(batches)
        >>> bchs
        []

        Yields
        ------
        Iterator[Iterable[Iterable[str]]]
            The $BATCH STREAAM$
        """
        at_least_n = 2
        for doc in docs:
            tokenlist = list(doc)
            docsize = len(tokenlist)
            # end_sliding = docsize+1-at_least_n+batchsize
            end = docsize+1
            for i in range(at_least_n, end):
                yield tokenlist[max(i-batchsize, 0):i]

    @classmethod
    def get_cobatches(
        cls,
        docs: Iterable[Iterable[str]],
        batchsize: int,
        offset: int
    ) -> Iterable[Tuple[Iterable[str], Iterable[str]]]:
        """Get a list of (anchorbatch, workingbatch)

        Parameters
        ----------
        docs : Iterable[Iterable[str]]
        batchsize : int
        offset : int
            Normally a multiple of the batchsize

        Example
        -------
        >>> docs = ['abcdefgeghieo', 'Hello world!']
        >>> batches = BatchMaker.get_cobatches(docs, batchsize=3, offset=3)
        >>> bchs = list(batches)
        >>> bchs[0]
        (['a', 'b', 'c'], ['d', 'e', 'f'])

        Yields
        ------
        Iterable[Tuple[Iterable[str],Iterable[str]]]
            ((<anchorbatch>, <workingbatch>))
        """
        for doc in docs:
            tokenlist = list(doc)
            docsize = len(tokenlist)
            for i in range(docsize-max(batchsize, offset)):
                yield (
                    # Anchor batch
                    tokenlist[i:i+batchsize],
                    # Working batch
                    tokenlist[i+offset:i+offset+batchsize]
                )


if __name__ == "__main__":
    import doctest
    doctest.testmod()
