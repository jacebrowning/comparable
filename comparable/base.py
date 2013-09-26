#!/usr/bin/env python

"""
Abstract base class and similarity functions.
"""


class _Base(object):
    """Shared base class."""

    def _repr(self, *args, **kwargs):
        """Return a __repr__ string from the arguments provided to __init__.
        @param args: list of arguments to __init__
        @param kwargs: dictionary of keyword arguments to __init__
        @return: __repr__ string
        """
        # Remove unnecessary empty keywords arguments
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        # Build the __repr__ string pieces
        args_repr = ', '.join(repr(arg) for arg in args)
        kwargs_repr = ', '.join(k + '=' + repr(v) for k, v in kwargs.items())
        if args_repr and kwargs_repr:
            kwargs_repr = ', ' + kwargs_repr
        name = self.__class__.__name__

        return "{}({}{})".format(name, args_repr, kwargs_repr)


class Similarity(_Base):
    """Represents the similarity between two objects."""

    def __init__(self, value, threshold=1.0):
        self.value = float(value)
        self.threshold = float(threshold)

    def __repr__(self):
        return self._repr(self.value, threshold=self.threshold)

    def __str__(self):
        return "{:.1%} similar".format(self.value)

    def __eq__(self, other):
        return abs(float(self) - float(other)) < 0.001

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return float(self) < float(other)

    def __gt__(self, other):
        return float(self) > float(other)

    def __bool__(self):
        """In boolean scenarios, similarity is True if the threshold is met.
        """
        return self.value >= self.threshold

    def __float__(self):
        """In non-boolean scenarios, similarity is treated like a float.
        """
        return self.value

    def __add__(self, other):
        return Similarity(self.value + float(other), threshold=self.threshold)

    def __radd__(self, other):
        return Similarity(float(other) + self.value, threshold=self.threshold)

    def __iadd__(self, other):
        self.value += float(other)
        return self

    def __sub__(self, other):
        return Similarity(self.value - float(other), threshold=self.threshold)

    def __rsub__(self, other):
        return Similarity(float(other) - self.value, threshold=self.threshold)

    def __isub__(self, other):
        self.value -= float(other)
        return self

    def __mul__(self, other):
        return Similarity(self.value * float(other), threshold=self.threshold)

    def __rmul__(self, other):
        return Similarity(float(other) * self.value, threshold=self.threshold)

    def __imul__(self, other):
        self.value *= float(other)
        return self

    def __abs__(self):
        return Similarity(abs(self.value), threshold=self.threshold)
