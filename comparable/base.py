#!/usr/bin/env python

"""
Abstract base class and similarity functions.
"""

import logging
from abc import ABCMeta, abstractmethod, abstractproperty


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


def equal(obj1, obj2):
    """Calculate equality between two (Comparable) objects.
    """
    logging.info("{} == {} : ...".format(repr(obj1), repr(obj2)))
    equality = obj1.equality(obj2)
    logging.info("{} == {} : {}".format(repr(obj1), repr(obj2), equality))
    return equality


def similar(obj1, obj2):
    """Calculate similarity between two (Comparable) objects.
    """
    logging.info("{} % {} : ...".format(repr(obj1), repr(obj2)))
    similarity = obj1.similarity(obj2)
    logging.info("{} % {} : {}".format(repr(obj1), repr(obj2), similarity))
    return similarity


class Comparable(_Base, metaclass=ABCMeta):
    """Abstract Base Class for objects that are comparable.

    Subclasses directly comparable should override the 'equality' and
    'similarity' methods to return a bool and 'Similarity' object,
    respectively.

    Subclasses comparable by attributes should override the
    'equality_list', 'similarity_dict', and 'similarity_threshold'
    properties to define which (Comparable) attributes should be considered.
    """

    def __eq__(self, other):
        """Maps the '==' operator to be a shortcut for "equality".
        """
        return equal(self, other)

    def __ne__(self, other):
        return not (self == other)

    def __mod__(self, other):
        """Maps the '%' operator to be a shortcut for "similarity".
        """
        return similar(self, other)

    @abstractproperty
    def equality_list(self):
        """Get the list of attributes names to consider in
        "equality" calculations.
        """
        return []

    @abstractmethod
    def equality(self, other, names=None):
        """Compare two objects for equality.
        @param self: first object to compare
        @param other: second object to compare
        @param attrs: list (or dict) of attributes names to consider
        @return: boolean result of comparison
        """

        if names is None:
            names = self.SIM_ATTRS

        if type(self) != type(other):
            logging.warning("types are different")
            return False

        for name in names:
            attr_1 = getattr(self, name)
            attr_2 = getattr(other, name)
            logging.debug("{}.{}: {} == {} : ...".format(self.__class__.__name__, name, repr(attr_1), repr(attr_2)))
            equality = attr_1 == attr_2
            logging.debug("{}.{}: {} == {} : {}".format(self.__class__.__name__, name, repr(attr_1), repr(attr_2), equality))
            if not equality:
                return False

        return True

    @abstractproperty
    def similarity_dict(self):
        """Get a dictionary of attribute {name: weight} to consider in
        "similarity" calculations.
        """
        return {}

    @abstractproperty
    def similarity_threshold(self):
        """Get the similarity threshold value for two objects to be
        considered "similar".
        """
        return 1.0

    @abstractmethod
    def similarity(self, other, names=None):
        """Compare two objects for similarity.
        @param self: first object to compare
        @param other: second object to compare
        @param names: dictionary of attribute {name: weight} to consider
        @return: L{Similarity} result of comparison
        """
        if names is None:
            names = self.SIM_ATTRS

        similarity = Similarity(0.0, self.THRESHOLD)
        total = 0.0

        # Calculate similarity ratio
        for name, weight in names.items():
            try:
                attr_1 = getattr(self, name)
                attr_2 = getattr(other, name)
            except AttributeError:
                logging.debug("{}.{}: skipped due to missing".format(self.__class__.__name__, name))
                continue
            logging.debug("{}.{}: {} % {} : ...".format(self.__class__.__name__, name, repr(attr_1), repr(attr_2)))
            if attr_1 is None or attr_2 is None:
                logging.debug("{}.{}: skipped due to None".format(self.__class__.__name__, name))
                continue
#             if not weight:
#                 logging.debug("{}.{}: skipped due to no weight".format(self.__class__.__name__, name))
#                 continue
            attr_similarity = attr_1 % attr_2
            logging.debug("{}.{}: {} % {} : {}".format(self.__class__.__name__, name, repr(attr_1), repr(attr_2), attr_similarity))
            total += weight
            similarity += attr_similarity * weight

        if total:
            similarity *= (1.0 / total)  # scale ratio so the total is 1.0

        return similarity


class SimpleComparable(Comparable):
    """Abstract Base Class for objects that are directly comparable.

    Subclasses must override the 'equality' and 'similarity' methods
    to return a bool and 'Similarity' object, respectively.
    """

    def equality_list(self):
        """A simple comparable does not use an equality list.
        """
        raise AttributeError()

    def similarity_dict(self):
        """A simple comparable does not use a similarity dict.
        """
        raise AttributeError()

    def similarity_threshold(self):
        """A simple comparable does not use a similarity threshold.
        """
        raise AttributeError()


class CompoundComparable(Comparable):
    """Abstract Base Class for objects that are comparable by attributes.

    Subclasses must override the 'equality_list', 'similarity_dict', and
    'similarity_threshold' properties to define which (Comparable)
    attributes should be considered.
    """

    def equality(self, other, *args, **kwargs):
        """A compound comparable's equality is based on attributes.
        """
        super().equality(self, other, *args, **kwargs)

    def similarity(self, other, *args, **kwargs):
        """A compound comparable's similarity is based on attributes.
        """
        super().similarity(self, other, *args, **kwargs)
