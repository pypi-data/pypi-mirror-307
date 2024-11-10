"""Utility."""


def capital_case(x: str) -> str:
    """Coerce string to capital case.

    Parameters
    ----------
    x : str
        Raw string.

    Returns
    -------
    str
        Capital-case string.

    Examples
    --------
    >>> capital_case('abc')
    'Abc'
    """
    return x.capitalize()
