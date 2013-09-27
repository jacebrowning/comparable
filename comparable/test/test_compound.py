#!/usr/bin/env python

"""
Unit tests for the comparable.extra module.
"""

import logging
import unittest

from comparable.simple import Text
from comparable.compound import Items

from comparable.test import TestCase, settings


class TestItems(TestCase):  # pylint: disable=R0904
    """Integration tests for the Items class."""

    def test_identical(self):
        """Verify two identical texts can be compared."""
        obj1 = Items(Text("abc"), Text("123"))
        obj2 = Items(Text("abc"), Text("123"))
        self.assertComparison(obj1, obj2, True, 1.00)


if __name__ == '__main__':
    logging.basicConfig(format=settings.VERBOSE_LOGGING_FORMAT,
                        level=settings.VERBOSE_LOGGING_LEVEL)
    unittest.main()
