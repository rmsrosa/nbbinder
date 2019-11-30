#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Used as waypoint for the relative imports through a parent directory
# Borrowed from https://docs.python-guide.org/writing/structure/
#

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import nbbinder