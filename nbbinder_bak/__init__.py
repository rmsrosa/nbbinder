#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gives a navigable book-like structure to a collection of Jupyter notebooks.
"""
__all__ = ['restructure', 'add_contents', 'add_headers', 'add_navigators',
    'bind']

from .nbbinder import *

__author__ = nbbinder.__author__
__homepage__ = nbbinder.__homepage__
__copyright__ = nbbinder.__copyright__
__license__ = nbbinder.__license__
__version__ = nbbinder.__version__

name = 'nbbinder'