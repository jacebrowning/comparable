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

    def __round__(self, digits):
        return Similarity(round(self.value, digits), threshold=self.threshold)


class _Indent():
    """Indent formatter for logging calls."""

    def __init__(self):
        self.level = 0

    def __str__(self):
        return '| ' * self.level

    def more(self):
        """Increase the indent level."""
        self.level += 1

    def less(self):
        """Decrease the indent level."""
        self.level = max(self.level - 1, 0)

_indent = _Indent()


def _log_cmp(obj1, obj2, op, cname=None, aname=None, result=None, level=None):
    """Log the objects being compared and the result.

    When no result object is specified, subsequence calls will have an
    increased indentation level. The indentation level is decreased
    once a result object is provided.

    @param obj1: first object
    @param obj2: second object
    @param op: operation being performed ('=' or '%')
    @param cname: name of class (when attributes are being compared)
    @param aname: name of attribute (when attributes are being compared)
    @param result: outcome of comparison
    @param level: logging level
    """
    fmt = "{o1} {op} {o2} : {r}"
    if cname or aname:
        assert cname and aname  # both must be specified
        fmt = "{c}.{a}: " + fmt
        level = level or logging.DEBUG
    else:
        level = level or logging.INFO

    if result is None:
        result = '...'
        indent = str(_indent)
        _indent.more()
    else:
        _indent.less()
        indent = str(_indent)

    logging.log(level, indent + fmt.format(o1=repr(obj1), o2=repr(obj2),
                                           c=cname, a=aname, op=op, r=result))


def equal(obj1, obj2):
    """Calculate equality between two (Comparable) objects.
    """
    _log_cmp(obj1, obj2, '=')
    equality = obj1.equality(obj2)
    _log_cmp(obj1, obj2, '=', result=equality)
    return equality


def similar(obj1, obj2):
    """Calculate similarity between two (Comparable) objects.
    """
    _log_cmp(obj1, obj2, '%')
    similarity = obj1.similarity(obj2)
    _log_cmp(obj1, obj2, '%', result=similarity)
    return similarity


class Comparable(_Base, metaclass=ABCMeta):
    """Abstract Base Class for objects that are comparable.

    Subclasses directly comparable must override the 'equality' and
    'similarity' methods to return a bool and 'Similarity' object,
    respectively.

    Subclasses comparable by attributes must override the
    'equality_list' and 'similarity_dict' properties to define which
    (Comparable) attributes should be considered. They may also
    override the 'similarity_threshold' property to change the default
    threshold.
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
    def equality_list(self):  # pragma: no cover, abstract
        """Get the list of attributes names to consider in
        "equality" calculations.
        """
        return []

    @abstractproperty
    def similarity_dict(self):  # pragma: no cover, abstract
        """Get a dictionary of attribute {name: weight} to consider in
        "similarity" calculations.
        """
        return {}

    @property
    def similarity_threshold(self):  # pragma: no cover, abstract
        """Get the similarity threshold value for two objects to be
        considered "similar".
        """
        return 1.0

    @abstractmethod
    def equality(self, other, names=None):
        """Compare two objects for equality.
        @param self: first object to compare
        @param other: second object to compare
        @param attrs: list of attributes names to consider
        @return: boolean result of comparison
        """
        if names is None:
            names = self.equality_list

        # Compare specified attributes for equality
        cname = self.__class__.__name__
        for aname in names:
            try:
                attr1 = getattr(self, aname)
                attr2 = getattr(other, aname)
            except AttributeError as error:
                logging.debug("{}.{}: {}".format(cname, aname, error))
                return False
            _log_cmp(attr1, attr2, '=', cname=cname, aname=aname)
            eq = (attr1 == attr2)
            _log_cmp(attr1, attr2, '=', cname=cname, aname=aname, result=eq)
            if not eq:
                return False

        return True

    @abstractmethod
    def similarity(self, other, names=None):
        """Compare two objects for similarity.
        @param self: first object to compare
        @param other: second object to compare
        @param names: dictionary of attribute {name: weight} to consider
        @return: L{Similarity} result of comparison
        """
        if names is None:
            names = self.similarity_dict

        sim = Similarity(0.0, self.similarity_threshold)
        total = 0.0

        # Calculate similarity ratio for specified attributes
        cname = self.__class__.__name__
        for aname, weight in names.items():

            # Handle for missing attributes
            try:
                attr1 = attr2 = '?'
                attr1 = getattr(self, aname)
                attr2 = getattr(other, aname)
            except AttributeError:
                _log_cmp(attr1, attr2, '%', cname=cname, aname=aname,
                         result="an attribute is missing")
                continue
            else:
                _log_cmp(attr1, attr2, '%', cname=cname, aname=aname)

            # Handle empty attributes
            if attr1 is None or attr2 is None:
                _log_cmp(attr1, attr2, '%', cname=cname, aname=aname,
                         result="an attribute is None")
                continue

            # Calculate similarity between the attributes
            attr_sim = (attr1 % attr2)
            _log_cmp(attr1, attr2, '%', cname=cname, aname=aname, result=sim)
            total += weight
            sim += attr_sim * weight

        if total:
            sim *= (1.0 / total)  # scale ratio so the total is 1.0

        return sim


class SimpleComparable(Comparable):
    """Abstract Base Class for objects that are directly comparable.

    Subclasses must override the 'equality' and 'similarity' methods
    to return a 'bool' and 'Similarity' object, respectively.
    """

    @property
    def equality_list(self):  # pragma: no cover, abstract
        """A simple comparable does not use an equality list.
        """
        raise AttributeError()

    @property
    def similarity_dict(self):  # pragma: no cover, abstract
        """A simple comparable does not use a similarity dict.
        """
        raise AttributeError()

    Similarity = Similarity  # constructor to create new similarities


class CompoundComparable(Comparable):
    """Abstract Base Class for objects that are comparable by attributes.

    Subclasses must override the 'equality_list', 'similarity_dict', and
    'similarity_threshold' properties to define which (Comparable)
    attributes should be considered.
    """

    def equality(self, other, *args, **kwargs):
        """A compound comparable's equality is based on attributes.
        """
        return super().equality(other, *args, **kwargs)

    def similarity(self, other, *args, **kwargs):
        """A compound comparable's similarity is based on attributes.
        """
        return super().similarity(other, *args, **kwargs)
