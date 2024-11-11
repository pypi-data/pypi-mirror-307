from typing import Callable, Iterator, TypeAlias

from textware.core import BatchMaker, NestedCounter, Transcessor

DocStream: TypeAlias = Iterator[str]


def distr_bay(
    docs: DocStream,
    batchsize: int = 5
) -> NestedCounter:
    """Build the bayesian distribution

    Parameters
    ----------
    docs : DocStream
        _description_
    batchsize : int, optional
        Size of the LearningWindow, by default 5

    Examples
    --------
    >>> cnt = distr_bay(('Hello world 42 ni hao servus!', 'Lorem ipsum ni hao'))
    >>> cnt['ni']['hao']
    2
    >>> cnt['world']['ni']
    1
    >>> dict(cnt['world']['ipsum'])
    {}
    >>> cnt['world'].get('42', 0)
    0
    >>> cnt['hello'].get('hao')
    1

    Returns
    -------
    NestedCounter
        _description_
    """

    cnt = NestedCounter()
    doctokens = Transcessor.get_words_from_docs(
        docs,
        filters=[Transcessor.remove_pure_nums]
    )
    for idx, batch in enumerate(BatchMaker.get_batches(doctokens, batchsize=batchsize)):
        keys = [(prio, batch[-1]) for prio in batch[0:-1]]
        cnt.update_from(keys)
    return cnt


def distr_bay_quantized(
    docs: DocStream,
    consolidator: Callable,
    docbatchsize: int = 1000,
    wordbatchsize: int = 5
) -> NestedCounter:
    cnt = NestedCounter()
    longterm = NestedCounter()
    for docbatch in BatchMaker.get_doc_batches(docs, batchsize=docbatchsize):
        batch_cnt = distr_bay(docbatch, batchsize=wordbatchsize)
        distilled = batch_cnt.consolidate_branches(selector=consolidator)
        longterm.update_fullpaths(distilled)
        cnt.update(batch_cnt)
    # Final consolidation
    distilled = cnt.consolidate_branches(selector=consolidator)
    longterm.update_fullpaths(distilled)
    return longterm
