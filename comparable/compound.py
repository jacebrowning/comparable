#!/usr/bin/env python

"""
Class definitions for compound comparable types.
"""

from comparable import CompoundComparable


class Group(CompoundComparable):
    """Comparable list of unordered Comparable items."""

    equality_list = ['items']
    similarity_dict = {'items': 1.0}

    def __init__(self, items):
        self.items = items
