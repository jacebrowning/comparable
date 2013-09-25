Introduction
============

Comparable is a library providing an abstract base class that enables
subclasses to be compared for "similarity" based on attributes. Similarity
is defined in each class to be a weighted average of attribute comparisons.



Getting Started
===============

Requirements
------------

* Python 3


Installation
------------

Comparable can be installed with ``pip``::

    pip install Comparable
    
After installation, Comparable can be used from its package::

    python
    >>> import comparable
    comparable.__version__
    >>> from comparable import Comparable

Comparable includes many generic comparable types::

   python
   >>> from comparable.basic import String, List
   >>> from comparable.extra import TitleString