"""parseparentheses.py

"""
# Package Header #
from ..header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from collections import deque
from functools import singledispatch
import re
from typing import Any, Generator, Iterable

# Third-Party Packages #

# Local Packages #


# Definitions #
# Functions #
def parentheses_iter(string: str) -> Generator[tuple[str, bool], None, None]:
    opens = re.finditer("\(", string)
    closes = re.finditer("\)", string)
    any_opens = True
    any_closes = True

    try:
        open_ = next(opens).start()
    except StopIteration:
        open_ = None
        any_opens = False

    try:
        close_ = next(closes).start()
    except StopIteration:
        close_ = None
        any_closes = False

    while any_opens or any_closes:
        if not any_opens or (any_closes and close_ < open_):
            yield close_, False

            try:
                close_ = next(closes).start()
            except StopIteration:
                close_ = None
                any_closes = False

        else:
            yield open_, True

            try:
                open_ = next(opens).start()
            except StopIteration:
                open_ = None
                any_opens = False


def decode_str_parentheses(string: str, iter_: Iterable, start: int = 0) -> tuple[deque, int]:
    items = deque()
    previous = start

    for location, is_open in iter_:
        if location > previous:
            items.append(string[previous:location])
            previous = location

        if is_open:
            item, previous = decode_str_parentheses(string, iter_, location + 1)
            if previous == -1:
                raise ValueError("unbalanced expression")
            items.append(item)
        else:
            return items, previous + 1
    return items, -1


def decode_bytes_parentheses(iter_: Iterable) -> tuple[deque, bool]:
    items = deque()
    b_item = b""
    ignore = False
    temp = None

    for b_as_i in iter_:
        if b_as_i in {34, 39}:
            if not ignore:
                ignore = True
                temp = b_as_i
            elif b_as_i == temp:
                ignore = False
                temp = None

        if not ignore and b_as_i == 40:
            if b_item:
                items.append(b_item)
                b_item = b""

            item, closed = decode_bytes_parentheses(iter_)

            if not closed:
                raise ValueError("unbalanced expression")

            items.append(item)
        elif not ignore and b_as_i == 41:
            if b_item:
                items.append(b_item)
                b_item = b""

            return items, True
        else:
            b_item += b_as_i.to_bytes(1, "little")
    return items, False


@singledispatch
def parse_parentheses(expression: str | bytes) -> dict[str, Any]:
    # Catch the general case for any unregistered types
    raise ValueError(f"{expression} is an invailid type")


@parse_parentheses.register
def _parse_parentheses(expression: str) -> dict[str, Any]:
    items, flag = decode_str_parentheses(expression, parentheses_iter(expression))
    if flag != -1:
        raise ValueError("unbalanced expression")
    return items


@parse_parentheses.register
def _parse_parentheses(expression: bytes) -> dict[str, Any]:
    items, flag = decode_bytes_parentheses(iter(expression))
    if flag:
        raise ValueError("unbalanced expression")
    return items
