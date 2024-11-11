"""
Parser types for command-line options, arguments and sub-commands

"""

# Class names are not CamelCase since they act as functions
# pylint: disable=invalid-name

import os
from argparse import Action, ArgumentTypeError

__all__ = [
    "is_int_positive",
    "is_int_positive_or_zero",
    "is_int_negative",
    "is_int_negative_or_zero",
    "is_file",
    "is_dir",
]


def _get_int_number(value: int, message: str) -> int:
    try:
        return int(value)
    except (ValueError, TypeError):
        raise ArgumentTypeError(message) from None


class is_int_positive(Action):
    """
    Verify that argument passed is a positive integer.

    Parameters
    ----------
    value: int
        value passed from argparser

    Returns
    -------
    int
        value passed from argparser

    Example
    -------

    .. code-block::

        parser.add_argument(
            "--size", "-s",
            dest="size",
            help="[MB] Minimal size of attachment",
            type=argtools.is_int_positive,
            default=100,
        )
    """

    def __call__(self, _parser, namespace, value, *args, **kwargs):
        message = f"value '{value}' must be positive"
        number = _get_int_number(value, message)
        if number <= 0:
            raise ArgumentTypeError(message) from None
        setattr(namespace, self.dest, number)


class is_int_positive_or_zero(Action):
    """
    Verify that argument passed is a positive integer or zero.

    Parameters
    ----------
    value: int
        value passed from argparser

    Returns
    -------
    int
        value passed from argparser

    Example
    -------

    .. code-block::

        parser.add_argument(
            "--size", "-s",
            dest="size",
            help="[MB] Minimal size of attachment",
            type=argtools.is_int_positive_or_zero,
            default=100,
        )
    """

    def __call__(self, _parser, namespace, value, *args, **kwargs):
        message = f"value '{value}' must be positive or zero"
        number = _get_int_number(value, message)
        if number < 0:
            raise ArgumentTypeError(message) from None
        setattr(namespace, self.dest, number)


class is_int_negative(Action):
    """
    Verify that argument passed is a negative integer.

    Parameters
    ----------
    value: int
        value passed from argparser

    Returns
    -------
    int
        value passed from argparser

    Example
    -------

    .. code-block::

        parser.add_argument(
            "--temperature", "-t",
            dest="temperature",
            help="[C] Temperature colder than freezing point",
            type=argtools.is_int_negative,
            default=-50,
        )
    """

    def __call__(self, _parser, namespace, value, *args, **kwargs):
        message = f"value '{value}' must be negative"
        number = _get_int_number(value, message)
        if number >= 0:
            raise ArgumentTypeError(message) from None
        setattr(namespace, self.dest, number)


class is_int_negative_or_zero(Action):
    """
    Verify that argument passed is a negative integer or zero.

    Parameters
    ----------
    value: int
        value passed from argparser

    Returns
    -------
    int
        value passed from argparser

    Example
    -------

    .. code-block::

        parser.add_argument(
            "--temperature", "-t",
            dest="temperature",
            help="[C] Temperature colder than freezing point",
            type=argtools.is_int_negative_or_zero,
            default=-50,
        )
    """

    def __call__(self, _parser, namespace, value, *args, **kwargs):
        message = f"value '{value}' must be negative or zero"
        number = _get_int_number(value, message)
        if number > 0:
            raise ArgumentTypeError(message) from None
        setattr(namespace, self.dest, number)


class is_file(Action):
    """
    Returns path if path is an existing regular file.
    This follows symbolic links

    Parameters
    ----------
    value: str
        value passed from argparser

    Returns
    -------
    str
        value passed from argparser

    Example
    -------

    .. code-block::

        parser.add_argument(
            "-f", "--file"
            type=argtools.is_file
        )
    """

    def __call__(self, _parser, namespace, value, *args, **kwargs):
        message = f"value '{value}' must be an existing file"
        if not os.path.isfile(str(value)):
            raise ArgumentTypeError(message) from None
        return value


class is_not_dir(Action):
    """
    Returns path if path is an existing file, including devices and not a directory.

    Parameters
    ----------
    value: str
        value passed from argparser

    Returns
    -------
    str
        value passed from argparser

    Example
    -------

    .. code-block::

        parser.add_argument(
            "-f", "--file"
            type=argtools.is_file
        )
    """

    def __call__(self, _parser, namespace, value, *args, **kwargs):
        message = f"value '{value}' must be an existing file"
        value = str(value)
        if not os.path.exists(str(value)):
            raise ArgumentTypeError(message) from None
        if os.path.isdir(str(value)):
            raise ArgumentTypeError(message) from None
        return value


class is_dir(Action):
    """
    Returns path if path is an existing regular directory.
    This follows symbolic links

    Parameters
    ----------
    value: str
        value passed from argparser

    Returns
    -------
    str
        value passed from argparser

    Example
    -------

    .. code-block::

        parser.add_argument(
            "-d", "--dir"
            type=argtools.is_dir
        )
    """

    def __call__(self, _parser, namespace, value, *args, **kwargs):
        message = f"value '{value}' must be an existing directory"
        if not os.path.isdir(str(value)):
            raise ArgumentTypeError(message) from None
        return value
