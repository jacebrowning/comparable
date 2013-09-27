#!/usr/bin/env python

"""
Unit tests for the comparable.basic module.
"""

import logging
import unittest

from comparable.simple import Number

from comparable.test import TestCase, settings


class TestNumber(TestCase):  # pylint: disable=R0904
    """Integration tests for the Number class."""

    def test_identical(self):
        """Verify two identical numbers can be compared."""
        obj1 = Number(42)
        obj2 = Number(42)
        self.assertComparison(obj1, obj2, True, 1.00)

    def test_different(self):
        """Verify two different numbers can be compared."""
        obj1 = Number(1)
        obj2 = Number(42)
        self.assertComparison(obj1, obj2, False, 0.02)

    def test_one_zero(self):
        """Verify zero can be compared with another number."""
        obj1 = Number(0)
        obj2 = Number(42)
        self.assertComparison(obj1, obj2, False, 0.00)

    def test_both_zero(self):
        """Verify two zero can be compared."""
        obj1 = Number(0)
        obj2 = Number(0)
        self.assertComparison(obj1, obj2, True, 1.00)

    def test_init_invalid(self):
        """Verify that a number can only be positive."""
        self.assertRaises(ValueError, Number, -1)

    def test_threshold(self):
        """Verify the Number threshold is correct."""
        self.assertTrue(Number(42) % Number(42.0001))
        self.assertFalse(Number(42) % Number(42.0005))

    def test_str(self):
        """Verify a Number can be converted to a string."""
        self.assertEqual("42.0", str(Number(42.0)))


if __name__ == '__main__':
    logging.basicConfig(format=settings.VERBOSE_LOGGING_FORMAT,
                        level=settings.VERBOSE_LOGGING_LEVEL)
    unittest.main()
