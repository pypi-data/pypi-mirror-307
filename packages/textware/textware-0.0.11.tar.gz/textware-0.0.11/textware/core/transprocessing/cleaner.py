import re


class Cleaner:
    """Collection of text pruning and cleaning funcs
    """

    @staticmethod
    def regularize(
        s: str,
        collapse_space: bool = False,
        no_tabs: bool = False
    ) -> str:
        """
        Cleans up the text.

        - remove duplicate linebreaks
        - (optionl) remove duplicated spaces
        - (optionl) replace tabs with spaces

        Parameters:
            s (str): The input string to clean.
            collapse_space(bool): If True, removes duplicate spaces within lines as well.
            no_tabs (bool): If True, replaces tabs with single spaces.

        Returns:
            str: The cleaned string.
        """

        s = re.sub(r'\n{2,}', '\n', s)

        if no_tabs:
            s = s.replace('\t', ' ')

        if collapse_space:
            s = re.sub(r' {2,}', ' ', s)

        return s

    @staticmethod
    def remove_empty_lines(s: str) -> str:
        return re.sub(r'^\s*\n', '', s, flags=re.MULTILINE)
