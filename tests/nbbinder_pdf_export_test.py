#!/anaconda3/envs/nbbinder/bin/python
# -*- coding: utf-8 -*-
'''
Notebook Binder test
'''

import os
import re
import logging

import shutil

from faker import Faker

import nbformat
from nbformat.v4.nbbase import new_markdown_cell

from context import nbbinder as nbb

# Logging level
logging.basicConfig(level=logging.WARNING)

def get_source_dir(path):
    return os.path.join('nb_source', path)

def get_build_dir(path: str='.'):
    return os.path.join('nb_builds', path)

def bind_test(source_dir, build_dir, config_file):

    if build_dir != source_dir:
        logging.info("\n# Copying source notebooks to build directory")

        shutil.copytree(source_dir, build_dir)

    logging.info("\n# Binding the notebooks in {} with '{}'".format(
        source_dir, config_file))

    nbb.bind(config_file)

if __name__ == '__main__':

    logging.info("# Changing to directory {}".format(os.path.dirname(__file__)))
    os.chdir(os.path.dirname(__file__))

    bind_test(get_source_dir('nb_water'), 
        get_build_dir('nb_water_export'),
        get_source_dir('config_nb_water_export.yml'))
