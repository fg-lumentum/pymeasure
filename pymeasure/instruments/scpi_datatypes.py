#
# This file is part of the PyMeasure package.
#
# Copyright (c) 2013-2025 PyMeasure Developers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

from enum import Enum
from dataclasses import dataclass


@dataclass(frozen=True)
class SCPIKeyword:

    keyword: str
    """The longform SCPI keyword, e.g. ``"VOLTage"``."""

    _REMOVE_LOWER = str.maketrans("", "", "abcdefghijklmnopqrstuvwxyz")

    def __init__(self, keyword):
        if isinstance(keyword, SCPIKeyword):
            object.__setattr__(self, "keyword", keyword.keyword)
            return

        if not isinstance(keyword, str):
            raise TypeError(f"Expected a string or SCPIKeyword, got {type(keyword).__name__}")

        if not keyword.isalnum():
            raise ValueError(f"Invalid SCPIKeyword '{keyword}': must be alphanumeric")

        upper = "".join(filter(str.isupper, keyword))
        lower = "".join(filter(str.islower, keyword))
        decimal = "".join(filter(str.isdecimal, keyword))

        if len(upper) == 0:
            raise ValueError(
                f"Invalid SCPIKeyword '{keyword}': "
                "Must start with at least one uppercase character."
            )

        if keyword != upper + lower + decimal:
            raise ValueError(
                f"Invalid SCPIKeyword '{keyword}': "
                "must be of the form '<uppercase><lowercase><decimal>'."
            )

        object.__setattr__(self, "keyword", keyword)

    @property
    def shortform(self):
        return self.keyword.translate(self._REMOVE_LOWER)

    def __eq__(self, other):
        if isinstance(other, SCPIKeyword):
            other = other.shortform
        return other == self.shortform

    def matches(self, value):
        if isinstance(value, SCPIKeyword):
            return value == self
        if isinstance(value, str):
            return value.upper() in (self.keyword.upper(), self.shortform)
        return TypeError(f"Expected type str or SCPIKeyword, got {type(value)}")

    def __hash__(self):
        return hash(self.shortform)

    def __str__(self):
        return self.shortform

    def __repr__(self):
        return f"SCPIKeyword('{self.keyword}')"


class SCPIKeywordEnum(SCPIKeyword, Enum):

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, (str, SCPIKeyword)):
            for member in cls:
                if member.value.matches(value):  # Uses SCPIKeyword.__eq__
                    return member
        return None

    def __str__(self):
        return str(self.value)
