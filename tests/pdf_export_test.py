#!/anaconda3/envs/nbbinder/bin/python
# -*- coding: utf-8 -*-
'''
PDF Export Binder test
'''

import os
import logging

import shutil

from context import nbbinder as nbb

# Logging level
logging.basicConfig(level=logging.WARNING)

# Build dir
BUILD_DIR = 'nb_export_builds'

def get_source_path(path):
    return os.path.join('nb_source', path)

def create_build_dir():
    if os.path.isdir(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)
    os.mkdir(BUILD_DIR)
    logging.info("Build directory {} created.".format(BUILD_DIR))

def get_build_path(path: str='.'):
    return os.path.join(BUILD_DIR, path)

def bind_test(source_path, build_path, config_file):

    if build_path != source_path:
        logging.info("\n# Copying source notebooks to build directory")

        shutil.copytree(source_path, build_path)

    logging.info("\n# Binding the notebooks in {} with '{}'".format(
        source_path, config_file))

    nbb.bind(config_file)

if __name__ == '__main__':

    logging.info("# Changing to directory '{}'".format(
        os.path.dirname(__file__)))
    os.chdir(os.path.dirname(__file__))

    logging.info("# Creating build directory '{}'.".format(BUILD_DIR))
    create_build_dir()

    bind_test(get_source_path('nb_water'), 
        get_build_path('nb_water_export'),
        get_source_path('config_nb_water_export.yml'))
