#!/usr/bin/env python

"""
Class definitions for compound comparable types.
"""

import logging
from itertools import permutations

from comparable.base import _log_cmp
from comparable import CompoundComparable


class Group(CompoundComparable):
    """Comparable list of Comparable items."""

    equality_list = None  # created dynamically
    similarity_dict = None  # created dynamically

    def __init__(self, items):
        self.items = items
        names = ["item{0}".format(n + 1) for n in range(len(items))]
        self.equality_list = names
        self.similarity_dict = {name: 1 for name in names}

    # TODO: refactor
    def __getattr__(self, name):
        """Allows self.items[<i>] to be accessed as self.item<i+1>.
        """
        if name.startswith('item'):
            try:
                return self.items[int(name.replace('item', '')) - 1]
            except (ValueError, IndexError):
                logging.debug("{0} cannot be mapped to an index in Group.items[]".format(repr(name)))
        raise AttributeError

    def __len__(self):
        return len(self.items)

    def equality(self, other, equality_list=None):
        """Calculate equality based on equality of all group items.
        """
        if not len(self) == len(other):
            return False
        return super().equality(other, equality_list=equality_list)

    # TODO: refactor
    def similarity(self, other, similarity_dict=None):
        """Calculate similarity based on similarity of the best matching
        permutation of items.
        """
        sim = self.Similarity(0.0, self.similarity_threshold)

        if len(self.items) > len(other.items):
            first, second = self, other
        else:
            first, second = other, self
        items = list(first.items)
        if not items:
            return self.Similarity(1.0, self.similarity_threshold)

        length = len(items)
        similarity_dict = {"item{}".format(i + 1): 1 for i in range(length)}
        logging.debug("similarity_dict: {}".format(similarity_dict))

        cname = self.__class__.__name__
        _log_cmp(first, second, '%', cname=cname, aname='items')

        for permutation in permutations(items, length):
            first.items = permutation

            logging.debug("permutation first: {}".format(repr(first.items)))
            logging.debug("permutation second: {}".format(repr(second.items)))

            sim = max(sim, super(Group, first).similarity(second, similarity_dict=similarity_dict))

            logging.debug("highest similarity: {0}".format(sim))

        _log_cmp(first, second, '%', cname=cname, aname='items', result=sim)

        logging.debug("similarity: {}".format(sim))
        first.items = items

        return sim
