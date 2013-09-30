#!/usr/bin/env python

"""
Tests for the comparable.compound module.
"""

import logging
import unittest

from comparable.simple import Text
from comparable.compound import Group

from comparable.test import TestCase, settings


class TestItems(TestCase):  # pylint: disable=R0904
    """Integration tests for the Items class."""

    def test_identical(self):
        """Verify two identical texts can be compared."""
        obj1 = Group([Text("abc"), Text("123")])
        obj2 = Group([Text("abc"), Text("123")])
        self.assertComparison(obj1, obj2, True, 1.00)


if __name__ == '__main__':
    logging.basicConfig(format=settings.VERBOSE_LOGGING_FORMAT,
                        level=settings.VERBOSE_LOGGING_LEVEL)
    unittest.main()
