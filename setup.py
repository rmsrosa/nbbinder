#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Based on *Packaging Python Projects*
# at https://packaging.python.org/tutorials/packaging-projects/
"""
Setup for NBBinder module
"""
import os
import re
import setuptools

import nbbinder as nbb


#def get_version(script: str) -> str:
#    """
#    Get the version number directly from the given script file
#    """
#    # Regular expression to capture version number
#    # Tested in https://regexr.com/
#    reg_version = re.compile(
#        r'\b(__version__\s*=\s*[\'"])([0-9]+[.][0-9]+(a|b|)[0-9]*)(["\'])')
#
#    basedir = os.path.dirname(__file__)
#    with open(os.path.join(basedir, script)) as f:
#        for line in f:
#            if reg_version.match(line):
#                return reg_version.match(line).group(2)
#    raise RuntimeError('No version info found.')


setuptools.setup(
    name='nbbinder',
    version=nbb.__version__,
    author='Ricardo M. S. Rosa',
    author_email='rmsrosa@gmail.com',
    description='Generates a navigable book-like structure \
        to a collection of jupyter notebooks',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/rmsrosa/nbbinder',
    project_urls={
        "Documentation": "https://nbbinder.readthedocs.io/",
        "Source Code": "https://github.com/rmsrosa/nbbinder",
    },
    py_modules=["nbbinder"],
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Development Status :: 3 - Alpha',
        'Framework :: Jupyter',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: MIT License'
    ],
    python_requires=">=3.5",
)
