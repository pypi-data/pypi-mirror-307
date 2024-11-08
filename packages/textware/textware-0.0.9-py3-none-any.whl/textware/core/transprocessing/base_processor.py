import re
from functools import reduce
from typing import Callable, Iterable, List


class Regex:
    puncs = re.compile(r'([.!?,:])(?=\s|$)')
    parenth_l = re.compile(r'(\s[\(\[])')
    parenth_r = re.compile(r'([\)\]]\s)')
    quotation_l = re.compile(r'(\s")')
    quotation_r = re.compile(r'("\s)')
    sentence_end = re.compile(r'(?<=[.?!]) +')
    sentence_end_one = re.compile(r'[\.\?!]')
    puncs_detached = re.compile(r'\s+([,.:;!?])(?=\s|$)')
    """From 'Hey , there !' -> 'Hey, there!'"""
    valid_word = re.compile(r'\w')
    digit = re.compile(r'\d')


def is_valid_word(text: str) -> bool:
    return (
        len(Regex.valid_word.findall(text)) > 0
    )


def is_text_word(text: str) -> bool:
    """Not a pure numerical number

    Parameters
    ----------
    text : str

    Returns
    -------
    bool
        True if it contains not only digits
    """
    nword = len(Regex.valid_word.findall(text))
    ndigit = len(Regex.digit.findall(text))
    return nword > ndigit


def normalize_punctuation(text: str) -> str:
    text = Regex.puncs.sub(r' \1 ', text)
    text = Regex.parenth_l.sub(r' \1 ', text)
    text = Regex.parenth_r.sub(r' \1 ', text)
    text = Regex.quotation_l.sub(r' \1 ', text)
    text = Regex.quotation_r.sub(r' \1 ', text)
    return text


def split_sentences(text: str) -> List[str]:
    sentences = Regex.sentence_end.split(text)
    sentences = [
        re.sub(r'(\W)$', r' \1', sent)
        for sent in sentences
    ]
    return sentences


def split_sentences_from_words(words: List[str]) -> List[List[str]]:
    """Split a list of words into list of list of words

    Parameters
    ----------
    words : List[str]

    Returns
    -------
    List[List[str]]
        Each sentence is a List[str]
    """
    result, current_group = [], []

    for item in words:
        if Regex.sentence_end_one.fullmatch(item):
            if current_group:
                result.append(current_group)
            current_group = []
        else:
            current_group.append(item)

    if current_group:
        result.append(current_group)
    return result


# Numbers
# ------------------------------------------------------------------------------


def mask_rest_digits(text):
    """
    Mask all following digits to '0', keeping the first intact.

    Args:
        text (str): The input string from which digits will be replaced.

    Returns:
        str: The modified string with specified digits replaced by '0'.

    Example:
    >>> mask_rest_digits("Hello 123, this is a test 4567.")
    'Hello 100, this is a test 4000.'
    >>> mask_rest_digits("No digits here!")
    'No digits here!'
    >>> mask_rest_digits("This costs $100 and $200.")
    'This costs $100 and $200.'
    >>> mask_rest_digits("Testing 5678 and 89.")
    'Testing 5000 and 80.'
    """
    return re.sub(r'(?<=\d)\d', '0', text)

# API
# ------------------------------------------------------------------------------


def sentencize(
    text: str
) -> List[str]:
    """Split $text$ to a list of sentences.

    Parameters
    ----------
    text : str

    Returns
    -------
    List[str]
        A list of sentences
    """
    return split_sentences(text)


def sentencize_from_tokens(words: List[str]) -> List[List[str]]:
    """Chunk the sentences from a list of tokenized sentences

    Parameters
    ----------
    words : List[str]
        _description_

    Examples
    --------
    >>> words = ['Hello', 'world', '!', 'I', '(', 'greet', 'back', ')', '40', 'and', '3.1000000', '.'] 
    >>> sentencize_from_tokens(words)
    [['Hello', 'world'], ['I', '(', 'greet', 'back', ')', '40', 'and', '3.1000000']]

    Returns
    -------
    List[List[str]]
        _description_
    """
    return split_sentences_from_words(words)


def wordify(
    text: str,
    filters: Iterable[Callable[..., bool]] = []
) -> List[str]:
    """Simple tokenization of $text$ to list of words. 

    Parameters
    ----------
    text : str

    Examples
    --------
    >>> wordify('Hello world! I (greet back) 42 and 3.1415926.')
    ['Hello', 'world', '!', 'I', '(', 'greet', 'back', ')', '40', 'and', '3.1000000', '.']
    >>> wordify('Hello world! I (greet back) 42 and 3.1415926.', filters=[is_valid_word])
    ['Hello', 'world', 'I', 'greet', 'back', '40', 'and', '3.1000000']

    Returns
    -------
    List[str]
        List of words
    """
    text = mask_rest_digits(text)
    text = normalize_punctuation(text)
    words = list(reduce(lambda rolling, flt: filter(flt, rolling),
                        filters,
                        text.split()))
    return words


def format_back(tokens: List[str]) -> str:
    """Reassemble the original text aka. `decode`.

    Parameters
    ----------
    text : str

    Examples
    --------
    >>> words = ['Hello', 'world', '!', 'I', '(', 'greet', 'back', ')', '40', 'and', '3.1000000', '.']
    >>> format_back(words)
    'Hello world! I ( greet back ) 40 and 3.1000000.'

    Returns
    -------
    str
        The original text
    """
    text = ' '.join(tokens)
    return Regex.puncs_detached.sub(r'\1', text)


class Transcessor:
    """Transforming processor
    """
    remove_pure_nums = is_text_word

    @classmethod
    def get_sentences(cls, text: str) -> List[str]:
        return sentencize(text)

    @classmethod
    def get_sentences_from_tokens(cls, words: List[str]) -> List[List[str]]:
        return sentencize_from_tokens(words)

    @classmethod
    def get_words(
        cls,
        text: str,
        filters: Iterable[Callable[..., bool]] = []
    ) -> List[str]:
        return wordify(text, filters)

    @classmethod
    def get_words_from_docs(
        cls,
        docstream: Iterable[str],
        filters: List = []
    ) -> Iterable[List[str]]:
        for doc in Transcessor.render(docstream):
            yield Transcessor.get_words(doc, filters=filters)

    @classmethod
    def formback(cls, tokens: List[str]) -> str:
        return format_back(tokens)

    @classmethod
    def render(
        cls,
        docstream: Iterable[str],
        renders: List[Callable] = [str.lower]
    ) -> Iterable[str]:
        for doc in docstream:
            for _render in renders:
                doc = _render(doc)
            yield doc

    @classmethod
    def flatten_words(cls, docstream: Iterable[str]) -> Iterable[str]:
        for doc in docstream:
            yield from Transcessor.get_words(text=doc)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
