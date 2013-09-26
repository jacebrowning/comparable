#!/usr/bin/env python

"""
Unit tests for the comparable.base module.
"""

import logging
import unittest
from unittest.mock import patch, Mock, MagicMock

from comparable.base import _Base, Similarity
from comparable.base import SimpleComparable, CompoundComparable

from comparable.test import TestCase
from comparable.test import settings


class TestBase(TestCase):  # pylint: disable=R0904
    """Unit tests for the Base class."""

    class Sample(_Base):  # pylint: disable=R0903
        """Test class to show __repr__ formatting."""

        def __init__(self, arg1, arg2, kwarg1=None, kwarg2=None):
            self.arg1 = arg1
            self.arg2 = arg2
            self.kwarg1 = kwarg1
            self.kwarg2 = kwarg2

        def __repr__(self):
            return self._repr(self.arg1, self.arg2, kwarg1=self.kwarg1, kwarg2=self.kwarg2)

        def __eq__(self, other):
            return self.__dict__ == other.__dict__

        def __ne__(self, other):
            return self.__dict__ != other.__dict__

    def test_repr_all_args(self):
        """Verify a class with arguments is represented."""
        Sample = self.Sample  # pylint: disable=C0103
        sample = Sample(123, 'abc', 456, 'def')
        self.assertEqual(sample, eval(repr(sample)))

    def test_repr_no_kwargs(self):
        """Verify a class with no keyword arguments is represented."""
        Sample = self.Sample  # pylint: disable=C0103
        sample = Sample(123, 'abc')
        self.assertEqual(sample, eval(repr(sample)))

    def test_repr_empty_args(self):
        """Verify a class with empty keyword arguments is represented."""
        Sample = self.Sample  # pylint: disable=C0103
        sample = Sample(123, 'abc', None, kwarg2=None)
        self.assertEqual(sample, eval(repr(sample)))


class TestSimilarity(TestCase):  # pylint: disable=R0904
    """Unit tests for the Similarity class."""

    def test_str(self):
        """Verify similarity objects can be represented as strings."""
        self.assertEqual("100.0% similar", str(Similarity(1.0)))
        self.assertEqual("99.0% similar", str(Similarity(0.99)))
        self.assertEqual("0.0% similar", str(Similarity(0.0)))

    def test_repr(self):
        """Verify object representation works for similarity objects."""
        sim = Similarity(0.89, threshold=0.87)
        self.assertEqual(sim, eval(repr(sim)))

    def test_bool_true(self):
        """Verify a similarity of 1.0 is True."""
        self.assertTrue(Similarity(1.0))

    def test_bool_false(self):
        """Verify a similarity of <1.0 if False."""
        self.assertFalse(Similarity(0.99))

    def test_bool_true_with_threshold(self):
        """Verify a similarity of <1.0 is True with a threshold."""
        self.assertTrue(Similarity(0.89, threshold=0.88))

    def test_bool_false_with_threshold(self):
        """Verify a similarity is False if under the threshold."""
        self.assertFalse(Similarity(0.89, threshold=0.90))

    def test_float_equal(self):
        """Verify similarities and floats can be compared for equality."""
        self.assertEqual(Similarity(0.42), 0.42)

    def test_float_not_equal(self):
        """Verify similarities and floats can be compared for inequality."""
        self.assertNotEqual(0.12, Similarity(0.13))

    def test_sorting(self):
        """Verify similarities can be sorted."""
        sims = [Similarity(1), Similarity(0), 0.5]
        sims.sort()
        self.assertEqual([Similarity(0), 0.5, Similarity(1)], sims)

    def test_add(self):
        """Verify two similarities can be added."""
        self.assertEqual(Similarity(0.42), Similarity(0.4) + Similarity(0.02))

    def test_add_with_number(self):
        """Verify a number can be added to a similarity."""
        self.assertEqual(Similarity(0.42), Similarity(0.4) + 0.02)

    def test_iadd(self):
        """Verify a similarity can be added to."""
        similarity = Similarity(0.4)
        similarity += Similarity(0.02)
        self.assertEqual(Similarity(0.42), similarity)

    def test_iadd_with_number(self):
        """Verify a similarity can be added to by a number."""
        similarity = Similarity(0.4)
        similarity += 0.02
        self.assertEqual(Similarity(0.42), similarity)

    def test_radd_with_number(self):
        """Verify a similarity can be added to a number."""
        self.assertEqual(Similarity(0.42), 0.4 + Similarity(0.02))

    def test_sub(self):
        """Verify two similarities can be subtracted."""
        self.assertEqual(Similarity(0.42), Similarity(0.43) - Similarity(0.01))

    def test_sub_with_number(self):
        """Verify a number can be subtracted from a similarity."""
        self.assertEqual(Similarity(0.42), Similarity(0.43) - 0.01)

    def test_isub(self):
        """Verify a similarity can be subtracted from."""
        similarity = Similarity(0.43)
        similarity -= Similarity(0.01)
        self.assertEqual(Similarity(0.42), similarity)

    def test_isub_with_number(self):
        """Verify a number can be subtracted from a similarity."""
        similarity = Similarity(0.43)
        similarity -= 0.01
        self.assertEqual(Similarity(0.42), similarity)

    def test_rsub_with_number(self):
        """Verify a similarity can be subtracted from a number."""
        self.assertEqual(Similarity(0.42), 0.43 - Similarity(0.01))

    def test_mul(self):
        """Verify two similarities can be multiplied."""
        self.assertEqual(Similarity(0.42), Similarity(0.6) * Similarity(0.7))

    def test_mul_with_number(self):
        """Verify a number can be multiplied with a similarity."""
        self.assertEqual(Similarity(0.42), Similarity(0.6) * 0.7)

    def test_imul(self):
        """Verify a similarity can be multiplied to."""
        similarity = Similarity(0.6)
        similarity *= Similarity(0.7)
        self.assertEqual(Similarity(0.42), similarity)

    def test_imul_with_number(self):
        """Verify a similarity can be multiplied to by a number."""
        similarity = Similarity(0.6)
        similarity *= 0.7
        self.assertEqual(Similarity(0.42), similarity)

    def test_rmul_with_number(self):
        """Verify a similarity can multiplied with a number."""
        self.assertEqual(Similarity(0.42), 0.6 * Similarity(0.7))

    def test_abs(self):
        """Verify absolute value works for similarities."""
        self.assertEqual(Similarity(0.42), abs(Similarity(-0.42)))


class TestSimpleComparable(TestCase):  # pylint: disable=R0904
    """Unit tests for the SimpleComparable class."""

    class Simple(SimpleComparable):
        equality = Mock()
        similarity = Mock()

    def setUp(self):
        self.obj1 = self.Simple()
        self.obj2 = self.Simple()

    def test_equality_true(self):
        """Verify two simple comparables can be compared for equality."""
        with patch.object(self.Simple, 'equality', Mock(return_value=True)):
            equality = (self.obj1 == self.obj2)
            self.obj1.equality.assert_called_once_with(self.obj2)
            self.assertTrue(equality)

    def test_equality_false(self):
        """Verify two simple comparables can be compared for non-equality."""
        with patch.object(self.Simple, 'equality', Mock(return_value=False)):
            equality = (self.obj1 == self.obj2)
            self.obj1.equality.assert_called_once_with(self.obj2)
            self.assertFalse(equality)


if __name__ == '__main__':
    logging.basicConfig(format=settings.VERBOSE_LOGGING_FORMAT,
                        level=settings.VERBOSE_LOGGING_LEVEL)
    unittest.main()
