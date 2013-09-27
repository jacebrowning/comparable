#!/usr/bin/env python

"""
Class definitions for simple comparable types.
"""

from difflib import SequenceMatcher

from comparable import SimpleComparable


class _Simple(SimpleComparable):
    """SimpleComparable with common magic methods implemented."""

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return self._repr(self.value)

    def __str__(self):
        return str(self.value)

    def __float__(self):
        return float(self.value)


class Number(_Simple):
    """Comparable positive numerical type."""

    similarity_threshold = 0.99999  # only care about the first 3 decimals

    def __init__(self, value):
        if value < 0:
            raise ValueError("Number objects can only be positive")
        super().__init__(value)

    def equality(self, other):
        """Get equality using floating point equality.
        """
        return float(self) == float(other)

    def similarity(self, other):
        """Get similarity as a ratio of the two numbers.
        """
        numerator, denominator = sorted((self.value, other.value))
        try:
            ratio = float(numerator) / denominator
        except ZeroDivisionError:
            ratio = 0.0 if numerator else 1.0
        similarity = self.Similarity(ratio, self.similarity_threshold)
        return similarity


class Text(_Simple):
    """Comparable generic text type."""

    similarity_threshold = 0.83  # "Hello, world!" ~ "hello world"

    def equality(self, other):
        """Get equality using string comparison.
        """
        return str(self) == str(other)

    def similarity(self, other):
        """Get similarity as a ratio of the two numbers.
        """
        ratio = SequenceMatcher(a=self.value, b=other.value).ratio()
        similarity = self.Similarity(ratio, self.similarity_threshold)
        return similarity
