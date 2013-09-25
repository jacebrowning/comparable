#!/usr/bin/env python

"""
Unit tests for the comparable.extra module.
"""

import logging
import unittest

from comparable.test import settings


if __name__ == '__main__':
    logging.basicConfig(format=settings.VERBOSE_LOGGING_FORMAT,
                        level=settings.VERBOSE_LOGGING_LEVEL)
    unittest.main()
