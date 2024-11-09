from random import choices

_LOREM_ = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent facilisis interdum mi, sit amet tincidunt purus luctus at. Curabitur vitae lacus in mauris tincidunt vehicula. Integer convallis ligula justo, sed bibendum est suscipit a. Fusce at dui vitae nisi consequat ullamcorper vel et augue. Suspendisse potenti. Nullam rutrum sem id metus venenatis feugiat. Cras scelerisque justo nec tellus viverra, in bibendum lectus dignissim. Phasellus auctor augue a odio convallis, a ultricies ex aliquet. Etiam vehicula libero euismod est efficitur, vel facilisis elit vehicula. Maecenas accumsan, libero in consequat dictum, lectus felis congue nulla, nec ornare eros arcu ac ex. Sed sollicitudin quam a elit suscipit, ac vestibulum dui laoreet. Phasellus accumsan blandit nisi, vitae posuere libero bibendum at."""


class DummyContentWriter:

    source = _LOREM_

    def give(k: int) -> str:
        return DummyContentWriter.source[0:k]

    def mul(s: str, times: int) -> str:
        return s * times

    def give_digits(k: int) -> str:
        """Without leading 0"""
        assert k > 0, f"Must be at least one, but got {k}"
        first = ''.join(choices('123456789', k=1))
        rest = ''.join(choices('0123456789', k=k-1))
        return first + rest
