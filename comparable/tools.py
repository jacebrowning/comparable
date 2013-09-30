#!/usr/bin/env python

"""
Functions to utilize lists of Comparable objects.
"""


def find_similar(base, items):
    """Get all similar item from a list of items.

    @param base: base item to locate best match
    @param items: list of items for comparison
    @return: most similar item
    """
    return [item for item in items if base.similarity(item)]


def match_similar(base, items):
    """Get the most similar matching item from a list of items.

    """
    finds = find_similar(base, items)
    if finds:
        return max(finds, key=base.similarity)
    else:
        return None


def matches(base, items):
    """Get all similar items from the given list of items.

    @param base: base item to locate matches
    @param items: list of items for comparison
    @return: list of matching items
    """
    return [item for item in items if item.similarity(base)]


def sort(base, items):
    """Get a sorted list of items ranked in descending similarity.

    @param base: base item to perform comparison against
    @param items: list of items to compare to the base
    @return: list of items sorted by similarity to the base
    """
    return sorted(items, key=base.similarity, reverse=True)
