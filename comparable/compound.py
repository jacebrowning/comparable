#!/usr/bin/env python

"""
Class definitions for compound comparable types.
"""

import logging
from itertools import permutations

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
                logging.debug("{0} cannot be mapped to an index in self.items[]".format(repr(name)))
                return None
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
        similarity = self.Similarity(0.0, self.similarity_threshold)

        if len(self.items) > len(other.items):
            bigger, smaller = self, other
        else:
            bigger, smaller = other, self
        items = list(bigger.items)
        length = len(items)
        similarity_dict = {"item{}".format(i + 1): 1 for i in range(length)}
        logging.debug("similarity_dict: {}".format(similarity_dict))

        for permutation in permutations(items, length):
            bigger.items = permutation

            logging.debug("permutation bigger: {}".format(repr(bigger.items)))
            logging.debug("permutation smaller: {}".format(repr(smaller.items)))

            similarity = max(similarity, super().similarity(smaller, similarity_dict=similarity_dict))

            logging.debug("highest similarity: {0}".format(similarity))

        logging.debug("similarity: {}".format(similarity))
        bigger.items = items

        return similarity
